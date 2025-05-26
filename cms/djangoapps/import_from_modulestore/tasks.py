"""
Tasks for course to library import.
"""
import mimetypes
import os
from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser


from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction, IntegrityError
from edx_django_utils.monitoring import set_code_owner_attribute_from_module
from lxml import etree
from lxml.etree import _ElementTree as XmlTree
from opaque_keys.edx.keys import UsageKey, LearningContextKey
from opaque_keys.edx.locator import CourseLocator, LibraryLocator, LibraryContainerLocator
from openedx_learning.api import authoring as authoring_api
from openedx_learning.api.authoring_models import (
    LearningPackage, Component, ComponentVersion, Container, PublishableEntityVersion
)
from user_tasks.tasks import UserTask, UserTaskStatus

from openedx.core.djangoapps.content_libraries.api import ContainerType
from openedx.core.djangoapps.content_libraries import api as libraries_api
from openedx.core.djangoapps.content_libraries.models import ContentLibrary
from openedx.core.djangoapps.content_staging import api as staging_api

from .constants import CONTENT_STAGING_PURPOSE_TEMPLATE
from .data import ImportProgressState, CompositionLevel
from .models import Import, PublishableEntityImport, PublishableEntityMapping, StagedContentForImport


log = get_task_logger(__name__)
parser = etree.XMLParser(strip_cdata=False)


class ImportFromModulestoreTask(UserTask):
    """
    Base class for import to library tasks.
    """

    @staticmethod
    def calculate_total_steps(arguments_dict):
        """
        Get number of in-progress steps in importing process, as shown in the UI.
        """
        return len(list(ImportStep))

    @classmethod
    def generate_name(cls, arguments_dict):
        """
        Create a name for this particular import task instance.

        Arguments:
            arguments_dict (dict): The arguments given to the task function

        Returns:
            str: The generated name
        """
        return str(arguments_dict)
        todo()
        library_id = arguments_dict.get('learning_package_id')
        import_id = arguments_dict.get('import_pk')
        return f'Import course to library (library_id={library_id}, import_id={import_id})'

    
from enum import Enum

class ImportStep(Enum):
    """
    Strings representation the state of an in-progress modulestore-to-learning-core import.

    We use these values to set UserTaskStatus.state.
    The other possible UserTaskStatus.state values are the built-in ones:
    UserTaskStatus.{PENDING,FAILED,CANCELED,SUCCEEDED}.
    """
    VALIDATING_INPUT = 'Validating import task parameters'
    CANCELLING_OLD = 'Cancelling any imports between same source and destination for this user'
    CLEANING = 'Cleaning previously staged content'
    LOADING = 'Loading legacy content'
    STAGING = 'Staging legacy content for import'
    PARSING = 'Parsing staged OLX'
    IMPORTING_STRUCTURE = 'Importing staged content structure'
    IMPORTING_ASSETS = 'Importing staged files and resources'
    ASSOCIATING_ASSETS = 'Associating files and resources with components'


@shared_task(base=ImportFromModulestoreTask, bind=True)
# Note: The decorator @set_code_owner_attribute cannot be used here because the UserTaskMixin
#   does stack inspection and can't handle additional decorators.
def import_from_modulestore(self, user_id: int, import_pk: int) -> None:
    """
    @@TODO
    """
    set_code_owner_attribute_from_module(__name__)

    status: UserTaskStatus = self.status
    status.set_state(ImportStep.VALIDATING_INPUT)
    try:
        modulestore_import = Import.objects.get(pk=import_pk)
    except Import.DoesNotExist:
        status.fail(f"Modulestore Import object with id={import_pk} does not exist")
        return
    modulestore_import.task_status = self.status
    modulestore_import.save(update_fields=['task_status'])
    source_context_key: LearningContextKey = modulestore_import.source_key
    if isinstance(source_context_key, CourseLocator):
        source_usage_key = source_context_key.make_usage_key('course', 'course')
    elif isinstance(source_context_key, LibraryLocator):
        source_usage_key = source_context_key.make_usage_key('library', 'library')
    else:
        status.fail(
            f"Not a valid source context key: {source_context_key}. "
            "Source key must reference a course or a legacy library."
        )
        return
    try:
        library: ContentLibrary = modulestore_import.target.contentlibrary
    except LearningPackage.contentlibrary.RelatedObjectDoesNotExist:
        status.fail(
            "Currently, the ModuleStore Import can only target a learning package that is associated "
            f"with a content library. LearningPackage with id={modulestore_import.target.id} is not connected "
            "to any ContentLibrary. This restriction may be relaxed in a future release."
        )
        return
    status.increment_completed_steps()

    status.set_state(ImportStep.CANCELLING_OLD)
    imports_to_cancel = Import.objects.filter(
        source_key=modulestore_import.source_key,
        target_change=modulestore_import.target_change,
        task_status__user=modulestore_import.task_status.user,
    ).exclude(
        task_status__state__in=(UserTaskStatus.CANCELED, UserTaskStatus.SUCCEEDED)
    ).exclude(
        pk=modulestore_import.pk
    )
    for incomplete_import in imports_to_cancel:
        incomplete_import.task_status.cancel()
    status.increment_completed_steps()

    status.set_state(ImportStep.CLEANING)
    modulestore_import.clean_related_staged_content()
    status.increment_completed_steps()

    status.set_state(ImportStep.LOADING)
    from xmodule.modulestore.django import modulestore
    try:
        legacy_root = modulestore().get_item(source_usage_key)
    except Exception:  # @@TODO
        status.fail("@@TODO")
        return
    if not legacy_root:
        status.fail("@@TODO")
        return
    status.increment_completed_steps()

    status.set_state(ImportStep.STAGING)
    staged_content = staging_api.stage_xblock_temporarily(
        legacy_root,
        modulestore_import.task_status.user.pk,
        purpose=CONTENT_STAGING_PURPOSE_TEMPLATE.format(source_key=source_context_key),
    )
    staged = StagedContentForImport.objects.create(
        staged_content=staged_content,
        modulestore_import=modulestore_import,
        source_usage_key=legacy_root.usage_key,
    )
    status.increment_completed_steps()

    status.set_state(ImportStep.PARSING)
    parser = etree.XMLParser(strip_cdata=False)
    try:
        node = etree.fromstring(staged.staged_content.olx, parser=parser)
    except:  # @@TODO
        status.fail("@@TODO")
    status.increment_completed_steps()

    status.set_state(ImportStep.IMPORTING_STRUCTURE)
    try:
        with authoring_api.bulk_draft_changes_for(modulestore_import.target.id) as change_log:
            modulestore_import.target_change = change_log
            modulestore_import.save(update_fields={'target_change'})
            _import_node(staged, node)
    except:  # @@TODO
        status.fail("@@TODO")
    status.increment_completed_steps()

    status.set_state(ImportStep.IMPORTING_ASSETS)
    content_by_filename = {}
    now = datetime.now(tz=timezone.utc)
    for staged_content_file_data in staging_api.get_staged_content_static_files(staged.staged_content.id):
        old_path = staged_content_file_data.filename
        file_data = staging_api.get_staged_content_static_file_data(staged.staged_content, old_path)
        if not file_data:
            log.error(f"Staged content {staged.staged_content.id} included referenced file {old_path}, but no file data was found.")
            continue
        filename = os.path.basename(old_path)
        media_type_str = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        media_type = authoring_api.get_or_create_media_type(media_type_str)
        content_by_filename[filename] = authoring_api.get_or_create_file_content(
            modulestore_import.target_id,
            media_type.id,
            data=file_data,
            created=now,
        )
    status.increment_completed_steps()

    status.set_state(ImportStep.ASSOCIATING_ASSETS)
    imported_versions = todo()
    for component_version in imported_versions:
        for filename, content in content_by_filename.items():
            filename_no_ext, _ = os.path.splitext(filename)
            olx = todo()
            if filename_no_ext not in olx:
                continue
            new_path = f"static/{filename}"
            try:
                authoring_api.create_component_version_content(component_version.pk, content.id, key=filename)
            except IntegrityError:
                pass  # Content already exists
    status.increment_completed_steps()


def _import_node(
    target: ContentLibrary,
    staged: StagedContentForImport, 
    node: XmlTree,
) -> PublishableEntityVersion | None:
    """
    @@TODO
    """
    try:
        container_type = ContainerType.from_source_olx_tag(node.tag)
    except ValueError:
        if node.tag not in {"course", "library_root"}:
            return _import_component(target, staged, node).publishable_entity
    children: list[PublishableEntityVersion] = []
    for child_node in node.getchildren():
        if child := _import_node(target, staged, child_node):
            children.append(child)
    if staged.modulestore_import.composition_level >= CompositionLevel(container_type):
        return _import_container(target, staged, node, container_type, children).publishable_entity
    return None


def _import_container(
    target: ContentLibrary,
    staged: StagedContentForImport,
    node: XmlTree,
    container_type: ContainerType,
    children: list[PublishableEntityVersion],
) -> Container:
    """
    @@TODO
    """
    now = datetime.now(tz=timezone.utc)  # @@TODO
    slug: str = node.get('url_name')
    title: str = node.get('display_name', node.tag)
    replace_existing = staged.modulestore_import.replace_existing
    user_id = staged.modulestore_import.status.user_id
    source_key = staged.modulestore_import.source_key.make_usage_key(node.tag, slug)
    target_key = LibraryContainerLocator(target.library_key, container_type, slug)
    try:
        container = libraries_api.get_container(target_key)
        container_existed = True
    except libraries_api.ContentLibraryContainerNotFound:
        container_existed = False
        container = libraries_api.create_container(
            library_key=target.library_key,
            container_type=container_type,
            slug=slug,
            title=title,
            created=now,
            user_id=user_id,
        )
    mapping, _ = PublishableEntityMapping.objects.get_or_create(
        source_usage_key=source_key,
        target_package=target.learning_package_id,
        target_entity=container.publishable_entity_id,
    )
    if container_existed and not replace_existing:
        return container.versioning.draft
    authoring_api.create_next_container_version(
        container.id,
        title=title,
        entity_rows=[
            authoring_api.ContainerEntityRow(entity_pk=child, version_pk=None)
            for child in children
        ],
        created=now,
        created_by=user_id,
    )
    container_version = libraries_api.container_override_func(
        container_version.container,
        title=display_name or f"New {container_type}",
        created=datetime.now(tz=timezone.utc),
        created_by=self.modulestore_import.user_id,
    )
    PublishableEntityImport.objects.create(
        modulestore_import=staged.modulestore_import,
        resulting_mapping=mapping,
        resulting_change=staged.modulestore_import.target_change.records.get(
            entity=container.publishable_entity_id,
        ),
    )
    return container_version


def _import_component(
    target: ContentLibrary,
    staged: StagedContentForImport,
    node: XmlTree,
) -> ComponentVersion | None:
    """
    Create a block in a library (@@TODO) from a staged content block.
    """
    block_type: str = node.tag
    block_id: str = node.url_name
    source_usage_key: UsageKey = staged.modulestore_import.source_key.make_usage_key(block_type, block_id)
    replace_existing = staged.modulestore_import.replace_existing
    component_type = authoring_api.get_or_create_component_type("xblock.v1", block_type)
    now = datetime.now(tz=timezone.utc)

    try:
        component = authoring_api.get_components(target.learning_package_id).get(
            component_type=component_type,
            local_key=block_id,
        )
        component_existed = True
    except Component.DoesNotExist:
        component_existed = False
        try:
            libraries_api.validate_can_add_block_to_library(target.library_key, block_type, block_id)
        except libraries_api.IncompatibleTypesError as e:
            log.error(f"Error validating block {block_type}:{block_id} for library {target.library_key}: {e}")
            return None
        component = authoring_api.create_component(
            staged.modulestore_import.target.id,
            component_type=component_type,
            local_key=block_id,
            created=now,
            created_by=staged.modulestore_import.task_status.user_id,
        )
    mapping, _ = PublishableEntityMapping.objects.get_or_create(
        source_usage_key=source_usage_key,
        target_package=target.learning_package_id,
        target_entity=component.publishable_entity_id,
    )
    if component_existed and not replace_existing:
        return component.versioning.draft
    component_version = libraries_api.set_library_block_olx(
        target.library_key.make_usage_key(block_type, block_id),
        etree.tostring(node),
    )
    PublishableEntityImport.objects.create(
        modulestore_import=staged.modulestore_import,
        resulting_mapping=mapping,
        resulting_change=staged.modulestore_import.target_change.records.get(
            entity=component.publishable_entity_id,
        ),
    )
    return component_version