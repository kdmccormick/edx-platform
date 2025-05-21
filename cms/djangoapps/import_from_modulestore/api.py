"""
API for course to library import.
"""
from typing import Sequence

from django.contrib.auth import AbstractUser
from opaque_keys.edx.locator import LibraryLocatorV2, LibraryCollectionLocator
from opaque_keys.edx.keys import LearningContextKey
from openedx_learning.api.authoring import get_collection
from user_tasks.tasks import UserTask

from openedx.core.djangoapps.content_libraries.api import get_library

from . import tasks
from .helpers import cancel_incomplete_old_imports
from .data import CompositionLevel, ImportData
from .models import Import as _Import
from .validators import validate_usage_keys_to_import



def start_import_from_modulestore(
    source_key: LearningContextKey,
    target_key: LibraryLocatorV2 | LibraryCollectionLocator,
    user: AbstractUser,
    composition_level: CompositionLevel,
    replace_existing: bool = False,
) -> tuple[ImportData, UserTask]:
    """
    Import staged content to a library from staged content.
    """
    if isinstance(target_key, LibraryCollectionLocator):
        target_package = get_library(target_key.library_key).learning_package
        target_collection = get_collection(target_package.id, target_key.collection_id)
    else:
        target_package = get_library(target_key).learning_package
        target_collection = None
    modulestore_import = _Import.objects.create(
        source_key=source_key,
        user=user.id,
        composition_level=composition_level,
        replace_existing=replace_existing,
        target=target_package,
        target_collection=target_collection,
    )
    return start_import_from_modulestore_task(modulestore_import)


def start_import_from_modulestore_task(modulestore_import: _Import) -> tuple[ImportData, UserTask]:
    """
    """
    cancel_incomplete_old_imports(modulestore_import)
    task = tasks.import_from_modulestore.delay(import_pk=modulestore_import.pk)
    return modulestore_import, task