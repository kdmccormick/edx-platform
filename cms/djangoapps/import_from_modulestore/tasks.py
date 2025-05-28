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
from opaque_keys.edx.locator import CourseLocator, LibraryLocator, LibraryUsageLocatorV2, LibraryContainerLocator
from openedx_learning.api import authoring as authoring_api
from openedx_learning.api.authoring_models import (
    Component,
    ComponentVersion,
    ContainerVersion,
    DraftChangeLog,
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
    Import a course or legacy library into a learning package based on params pointed to by import_pk.

    Currently, the target learning package must be associated with a V2 content library, but that
    restriction may be loosened in the future as more types of learning packages are developed.
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
    if modulestore_import.task_status:
        status.fail(f"Import has already been executed: {modulestore_import!r}")
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
        task_status__user=status.user,
    ).exclude(
        task_status__state__in=(UserTaskStatus.CANCELED, UserTaskStatus.SUCCEEDED)
    ).exclude(
        pk=modulestore_import.pk
    )
    for incomplete_import in imports_to_cancel:
        if incomplete_import.task_status:
            incomplete_import.task_status.cancel()
    status.increment_completed_steps()

    status.set_state(ImportStep.CLEANING)
    modulestore_import.clean_related_staged_content()
    status.increment_completed_steps()

    status.set_state(ImportStep.LOADING)
    try:
        legacy_root = modulestore().get_item(source_usage_key)
    except modulestore_exceptions.ItemNotFoundError as exc:
        status.fail(f"Failed to load source item '{source_usage_key}' from ModuleStore: {exc}")
        return
    if not legacy_root:
        status.fail(f"Could not find source item '{source_usage_key}' in ModuleStore")
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
    except etree.ParseError as exc:
        status.fail(f"Failed to parse source OLX (from staged content with id = {staged.staged_content.id}): {exc}")
    status.increment_completed_steps()

    status.set_state(ImportStep.IMPORTING_ASSETS)
    content_by_filename: dict[str, int] = {}
    now = datetime.now(tz=timezone.utc)
    for staged_content_file_data in staging_api.get_staged_content_static_files(staged.staged_content.id):
        old_path = staged_content_file_data.filename
        file_data = staging_api.get_staged_content_static_file_data(staged.staged_content_id, old_path)
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

    class Nope(Exception): pass
    try:
        with authoring_api.bulk_draft_changes_for(modulestore_import.target.id) as change_log:
            _import_node(
                modulestore_import=modulestore_import,
                content_by_filename=content_by_filename,
                source_node=root_node,
                target_library=library,
                target_change=change_log,
                created_at=datetime.now(timezone.utc),
                created_by=status.user_id,
            )
    except Nope: # Exception as exc:  # pylint: disable=broad-except
        status.fail("@@TODO {exc}")
    modulestore_import.target_change = change_log
    status.increment_completed_steps()


def _import_node(
    modulestore_import: Import,
    content_by_filename: dict[str, int],
    source_node: XmlTree,
    target_library: ContentLibrary,
    target_change: DraftChangeLog,
    created_at: datetime,
    created_by: int,
) -> PublishableEntityVersion | None:
    """
    @@TODO

    Returns: The entity version corresponding to this particular `source_node`, or None if
    the node is not to be represented in the target package. IMPORTANT: Even if the result is
    None, descendents of `source_node` may have been imported into the target package. This
    will happen for any container which is above the specific `CompositionLevel`, as well as
    for the source course/library root block.
    """
    # The OLX tag will map to one of the following...
    #   * A wiki tag                  --> Ignore
    #   * A recognized container type --> Import children, and import container if requested.
    #   * A legacy library root       --> Import children, but NOT the root itself.
    #   * A course root               --> Import children, but NOT the root itself (for Teak, at least. Future
    #                                     releases may support treating the Course as an importable container).
    #   * Something else              --> Try to import it as a component. If that fails, then it's either an un-
    #                                     supported component type, or it's an XBlock with dynamic children, which we
    #                                     do not support in libraries as of Teak.
    import_node: bool
    import_children: bool
    container_type: ContainerType | None  # if None, import as Component
    if source_node.tag == "wiki":
        return None
    try:
        container_type = ContainerType.from_source_olx_tag(source_node.tag)
    except ValueError:
        container_type = None
        if source_node.tag in {"course", "library"}:
            import_node = False
            import_children = True
        else:
            import_node = True
            import_children = False
    else:
        this_level = CompositionLevel(container_type.value)
        requested_level = CompositionLevel(modulestore_import.composition_level)
        import_node = not this_level.is_higher_in_course_hierarchy(requested_level)
        import_children = True
    children: list[PublishableEntityVersion] = []
    if import_children:
        for child_node in source_node.getchildren():
            if child := _import_node(
                modulestore_import=modulestore_import,
                content_by_filename=content_by_filename,
                source_node=child_node,
                target_library=target_library,
                target_change=target_change,
                created_by=created_by,
                created_at=created_at,
            ):
                children.append(child)
    result: PublishableEntityVersion | None = None
    if import_node:
        if not (source_block_id := source_node.get('url_name')):
            # @@TODO fail more gracefully and/or have a fallback
            raise ValueError(f"node is missing url_name: {etree.tostring(source_node)}")
        source_usage_key: UsageKey = modulestore_import.source_key.make_usage_key(source_node.tag, source_block_id)
        if container_type:
            if result_container := _import_container(
                source_key=source_usage_key,
                container_type=container_type,
                title=source_node.get('display_name', source_block_id),
                children=children,
                target_library=target_library,
                replace_existing=modulestore_import.replace_existing,
                created_by=created_by,
                created_at=created_at,
            ):
                result = result_container.publishable_entity_version
        else:
            if result_component := _import_component(
                content_by_filename=content_by_filename,
                source_key=source_usage_key,
                olx=etree.tostring(source_node).decode('utf-8'),
                target_library=target_library,
                replace_existing=modulestore_import.replace_existing,
                created_by=created_by,
                created_at=created_at,
            ):
                result = result_component.publishable_entity_version
    if result:
        mapping, _ = PublishableEntityMapping.objects.get_or_create(
            source_usage_key=source_usage_key,
            target_package_id=modulestore_import.target_id,
            target_entity_id=result.entity_id,
        )
        PublishableEntityImport.objects.create(
            modulestore_import=modulestore_import,
            resulting_mapping=mapping,
            resulting_change=target_change.records.get(entity_id=result.entity_id),
        )
        if target_collection := modulestore_import.target_collection:
            # @@TODO - should we do this in bulk for efficiency?
            authoring_api.add_to_collection(
                learning_package_id=modulestore_import.target_id,
                key=target_collection.key,
                entities_qset=PublishableEntity.objects.filter(id=result.entity_id),
                created_by=created_by,
            )
    return result


def _import_container(
    source_key: UsageKey,
    container_type: ContainerType,
    title: str,
    children: list[PublishableEntityVersion],
    target_library: ContentLibrary,
    replace_existing: bool,
    created_by: int,
    created_at: datetime,
) -> ContainerVersion:
    """
    @@TODO
    """
    target_key = LibraryContainerLocator(target_library.library_key, container_type.value, source_key.block_id)
    try:
        container = libraries_api.get_container(target_key)
        container_existed = True
    except libraries_api.ContentLibraryContainerNotFound:
        container_existed = False
        container = libraries_api.create_container(
            library_key=target_library.library_key,
            container_type=container_type,
            slug=target_key.container_id,
            title=title,
            created=created_at,
            user_id=created_by,
        )
    if container_existed and not replace_existing:
        return ContainerVersion.objects.get(
            container_id=container.container_pk,
            publishable_entity_version__version_num=container.draft_version_num,
        )
    container_version: ContainerVersion = authoring_api.create_next_container_version(
        container.container_pk,
        title=title,
        entity_rows=[
            authoring_api.ContainerEntityRow(entity_pk=child.entity_id, version_pk=None)
            for child in children
        ],
        created=created_at,
        created_by=created_by,
    )
    return container_version


def _import_component(
    content_by_filename: dict[str, int],
    source_key: UsageKey,
    olx: str,
    target_library: ContentLibrary,
    replace_existing: bool,
    created_by: int,
    created_at: datetime,
) -> ComponentVersion | None:
    """
    Create a block in a library (@@TODO) from a staged content block.
    """
    component_type = authoring_api.get_or_create_component_type("xblock.v1", source_key.block_type)
    # We have ensured earlier in this task that the library's learning_package_id is not None.
    target_package_id: int = target_library.learning_package_id  # type: ignore[assignment]
    try:
        component = authoring_api.get_components(target_package_id).get(
            component_type=component_type,
            local_key=source_key.block_id,
        )
        component_existed = True
    except Component.DoesNotExist:
        component_existed = False
        try:
            libraries_api.validate_can_add_block_to_library(
                target_library.library_key, source_key.block_type, source_key.block_id
            )
        except libraries_api.IncompatibleTypesError as e:
            log.error(f"Error validating block  for library {target_library.library_key}: {e}")
            return None
        component = authoring_api.create_component(
            target_package_id,
            component_type=component_type,
            local_key=source_key.block_id,
            created=created_at,
            created_by=created_by,
        )
    if component_existed and not replace_existing:
        return component.versioning.draft
    component_version = libraries_api.set_library_block_olx(
        # mypy thinks LibraryUsageLocatorV2 is abstract. It's not.
        LibraryUsageLocatorV2(  # type: ignore[abstract]
            target_library.library_key, source_key.block_type, source_key.block_id
        ),
        new_olx_str=olx,
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
