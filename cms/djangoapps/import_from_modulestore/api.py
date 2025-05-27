"""
API for course to library import.
"""
from opaque_keys.edx.locator import LibraryLocatorV2, LibraryCollectionLocator
from opaque_keys.edx.keys import LearningContextKey
from openedx_learning.api.authoring import get_collection
from user_tasks.tasks import UserTask

from openedx.core.djangoapps.content_libraries.api import get_library
from openedx.core.types.user import AuthUser

from . import tasks
from .data import CompositionLevel
from .models import Import as _Import


def start_import_from_modulestore(
    source_key: LearningContextKey,
    target_key: LibraryLocatorV2 | LibraryCollectionLocator,
    user: AuthUser,
    composition_level: CompositionLevel,
    replace_existing: bool = False,
) -> tuple[_Import, UserTask]:
    """
    Import staged content to a library from staged content.
    """
    target_library = get_library(
        target_key.lib_key if isinstance(target_key, LibraryCollectionLocator) else target_key
    )
    if not (target_package_id := target_library.learning_package_id):
        raise ValueError(
            f"Cannot import {source_key} into library at {target_key} because the "
            "library is not connected to a learning packge"
        )
    if isinstance(target_key, LibraryCollectionLocator):
        target_collection_id = get_collection(target_package_id, target_key.collection_id).id
    modulestore_import = _Import.objects.create(
        source_key=source_key,
        composition_level=composition_level.value,
        replace_existing=replace_existing,
        target_id=target_package_id,
        target_collection_id=target_collection_id,
    )
    return start_import_from_modulestore_task(user, modulestore_import)


def start_import_from_modulestore_task(user: AuthUser, modulestore_import: _Import) -> tuple[_Import, UserTask]:
    """
    @@TODO
    """
    task = tasks.import_from_modulestore.delay(user_id=user.id, import_pk=modulestore_import.pk)
    return modulestore_import, task
