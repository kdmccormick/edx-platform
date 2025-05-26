"""
Tasks for course to library import.
"""
import mimetypes
import os
from datetime import datetime, timezone
from enum import Enum


from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import IntegrityError
from edx_django_utils.monitoring import set_code_owner_attribute_from_module
from lxml import etree
from lxml.etree import _ElementTree as XmlTree
from opaque_keys.edx.keys import UsageKey, LearningContextKey
from opaque_keys.edx.locator import CourseLocator, LibraryLocator, LibraryContainerLocator
from openedx_learning.api import authoring as authoring_api
from openedx_learning.api.authoring_models import (
    Component,
    ComponentVersion,
    ContainerVersion,
    LearningPackage,
    PublishableEntity,
    PublishableEntityVersion,
)
from user_tasks.tasks import UserTask, UserTaskStatus

from openedx.core.djangoapps.content_libraries.api import ContainerType
from openedx.core.djangoapps.content_libraries import api as libraries_api
from openedx.core.djangoapps.content_libraries.models import ContentLibrary
from openedx.core.djangoapps.content_staging import api as staging_api
from xmodule.modulestore import exceptions as modulestore_exceptions
from xmodule.modulestore.django import modulestore

from .constants import CONTENT_STAGING_PURPOSE_TEMPLATE
from .data import CompositionLevel
from .models import Import, PublishableEntityImport, PublishableEntityMapping, StagedContentForImport


log = get_task_logger(__name__)


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
    IMPORTING_ASSETS = 'Importing staged files and resources'
    IMPORTING_STRUCTURE = 'Importing staged content structure'


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
        import_pk = arguments_dict["import_pk"]
        try:
            modulestore_import = Import.objects.get(id=import_pk)
        except Import.DoesNotExist:
            return f"ModuleStore Import task with invalid import_pk {import_pk}"
        return f"ModuleStore Import: {modulestore_import.source_key} -> {modulestore_import.target.key}"


@shared_task(base=ImportFromModulestoreTask, bind=True)
# Note: The decorator @set_code_owner_attribute cannot be used here because the UserTaskMixin
#   does stack inspection and can't handle additional decorators.
def import_from_modulestore(self, user_id: int, import_pk: int) -> None:
    """
    @@TODO
    """
    # pylint: disable=too-many-statements
    # This is a large function, but breaking it up futher would probably not
    # make it any easier to understand.

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
    try:
        legacy_root = modulestore().get_item(source_usage_key)
    except modulestore_exceptions.ItemNotFoundError:
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
        root_node = etree.fromstring(staged.staged_content.olx, parser=parser)
    except etree.ParseError as exc:  # @@TODO
        status.fail(f"@@TODO {exc}")
    status.increment_completed_steps()

    status.set_state(ImportStep.IMPORTING_ASSETS)
    content_by_filename: dict[str, int] = {}
    now = datetime.now(tz=timezone.utc)
    for staged_content_file_data in staging_api.get_staged_content_static_files(staged.staged_content.id):
        old_path = staged_content_file_data.filename
        file_data = staging_api.get_staged_content_static_file_data(staged.staged_content, old_path)
        if not file_data:
            log.error(
                f"Staged content {staged.staged_content.id} included referenced file {old_path}, "
                "but no file data was found."
            )
            continue
        filename = os.path.basename(old_path)
        media_type_str = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        media_type = authoring_api.get_or_create_media_type(media_type_str)
        content_by_filename[filename] = authoring_api.get_or_create_file_content(
            modulestore_import.target_id,
            media_type.id,
            data=file_data,
            created=now,
        ).id
    status.increment_completed_steps()

    status.set_state(ImportStep.IMPORTING_STRUCTURE)
    try:
        with authoring_api.bulk_draft_changes_for(modulestore_import.target.id) as change_log:
            modulestore_import.target_change = change_log
            modulestore_import.save(update_fields={'target_change'})
            _import_node(
                staged=staged,
                content_by_filename=content_by_filename,
                source_node=root_node,
                target=library,
            )
    except exc:  # pylint: disable=bare-except
        status.fail("@@TODO {exc}")
    status.increment_completed_steps()


def _import_node(
    staged: StagedContentForImport,
    content_by_filename: dict[str, int],
    source_node: XmlTree,
    target: ContentLibrary,
) -> PublishableEntityVersion | None:
    """
    @@TODO

    Returns: The entity version corresponding to this particular `source_node`, or None if
    the node is not to be represented in the target package. IMPORTANT: Even if the result is
    None, descendents of `source_node` may have been imported into the target package. This
    will happen for any container which is above the specific `CompositionLevel`, as well as
    for the source course/library root block.
    """
    result: PublishableEntityVersion | None = None
    try:
        container_type = ContainerType.from_source_olx_tag(source_node.tag)
    except ValueError:
        # If the OLX tag is not a recognized container, then it is one of the following:
        # * A legacy library root, which has no semantic meaning on its own... we import its children
        #   but not the library root block itself.
        # * A course root, which may be considered a 'container' in a future release... but as of Teak,
        #   we just import its children and ignore the course root block itself.
        # * A component, which we will try to import... although the target package may reject it if it's
        #   an unsupported component type.
        # * A dynamic block (e.g. SplitTest)... as of Teak, these are not supported and will be skipped.
        if source_node.tag in {"course", "library_root"}:
            # Course or library root -- skip and just import children.
            result = None
        else:
            # Component or dynamic block. Assume component... _import_component will skip it if it's an
            # unsupported component type or a dynamic block.
            # (@@TODO if it's a dynamic block, should we be importing its children...?)
            result = _import_component(
                staged=staged,
                content_by_filename=content_by_filename,
                source_node=source_node,
                target=target,
            ).publishable_entity
    else:
        children: list[PublishableEntityVersion] = []
        for child_node in source_node.getchildren():
            if child := _import_node(
                staged=staged,
                content_by_filename=content_by_filename,
                source_node=child_node,
                target=target,
            ):
                children.append(child)
        if staged.modulestore_import.composition_level >= CompositionLevel(container_type):
            result = _import_container(
                staged=staged,
                source_node=source_node,
                container_type=container_type,
                children=children,
                target=target,
            ).publishable_entity_version
        else:
            result = None
    if result:
        # @@TODO - should we do this in bulk for efficiency?
        authoring_api.add_to_collection(
            staged.modulestore_import.target,
            staged.modulestore_import.target_collection.key,
            PublishableEntity.objects.filter(id=result.id),
            created_by=staged.modulestore_import.task_status.user_id,
        )
    return result


def _import_container(
    staged: StagedContentForImport,
    source_node: XmlTree,
    container_type: ContainerType,
    children: list[PublishableEntityVersion],
    target: ContentLibrary,
) -> ContainerVersion:
    """
    @@TODO
    """
    now = datetime.now(tz=timezone.utc)
    slug: str = source_node.get('url_name')
    title: str = source_node.get('display_name', source_node.tag)
    replace_existing = staged.modulestore_import.replace_existing
    user_id = staged.modulestore_import.status.user_id
    source_key = staged.modulestore_import.source_key.make_usage_key(source_node.tag, slug)
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
    container_version = authoring_api.create_next_container_version(
        container.id,
        title=title,
        entity_rows=[
            authoring_api.ContainerEntityRow(entity_pk=child, version_pk=None)
            for child in children
        ],
        created=now,
        created_by=user_id,
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
    staged: StagedContentForImport,
    content_by_filename: dict[str, int],
    source_node: XmlTree,
    target: ContentLibrary,
) -> ComponentVersion | None:
    """
    Create a block in a library (@@TODO) from a staged content block.
    """
    block_type: str = source_node.tag
    block_id: str = source_node.url_name
    source_usage_key: UsageKey = staged.modulestore_import.source_key.make_usage_key(block_type, block_id)
    replace_existing = staged.modulestore_import.replace_existing
    component_type = authoring_api.get_or_create_component_type("xblock.v1", block_type)

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
            created=datetime.now(tz=timezone.utc),
            created_by=staged.modulestore_import.task_status.user_id,
        )
    mapping, _ = PublishableEntityMapping.objects.get_or_create(
        source_usage_key=source_usage_key,
        target_package=target.learning_package_id,
        target_entity=component.publishable_entity_id,
    )
    if component_existed and not replace_existing:
        return component.versioning.draft
    olx_bytes: bytes = etree.tostring(source_node)
    olx: str = olx_bytes.decode('utf-8')
    component_version = libraries_api.set_library_block_olx(
        target.library_key.make_usage_key(block_type, block_id),
        olx_bytes,
    )
    PublishableEntityImport.objects.create(
        modulestore_import=staged.modulestore_import,
        resulting_mapping=mapping,
        resulting_change=staged.modulestore_import.target_change.records.get(
            entity=component.publishable_entity_id,
        ),
    )
    for filename, content_pk in content_by_filename.items():
        filename_no_ext, _ = os.path.splitext(filename)
        if filename_no_ext not in olx:
            continue
        new_path = f"static/{filename}"
        try:
            authoring_api.create_component_version_content(component_version.pk, content_pk, key=filename)
        except IntegrityError:
            pass  # Content already exists
    return component_version
