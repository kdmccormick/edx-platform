"""
API Client for Blockstore

This API does not do any caching; consider using BundleCache or (in
openedx.core.djangolib.blockstore_cache) together with these API methods for
improved performance.

TODO: This wrapper is extraneous now that Blockstore-as-a-service isn't supported.
      This whole directory tree should be removed by https://github.com/openedx/blockstore/issues/296.
"""
from blockstore.apps.api.data import BundleFileData
from blockstore.apps.api.exceptions import (
    BundleFileNotFound,
    BundleNotFound,
    BundleStorageError,
    BundleVersionNotFound,
    CollectionNotFound,
    DraftNotFound,
)
from blockstore.apps.api.methods import (  # Collections:; Bundles:; Drafts:; Bundles or drafts:; Links:; Misc:
    commit_draft,
    create_bundle,
    create_collection,
    delete_bundle,
    delete_collection,
    delete_draft,
    force_browser_url,
    get_bundle,
    get_bundle_file_data,
    get_bundle_file_metadata,
    get_bundle_files,
    get_bundle_files_dict,
    get_bundle_links,
    get_bundle_version,
    get_bundle_version_files,
    get_bundle_version_links,
    get_bundles,
    get_collection,
    get_draft,
    get_or_create_bundle_draft,
    set_draft_link,
    update_bundle,
    update_collection,
    write_draft_file,
)
