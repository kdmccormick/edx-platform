"""
Tests for library tools service (only used by CMS)

Currently, the only known user of the LibraryToolsService is the
LibraryContentBlock, so these tests are all written with only that
block type in mind.
"""

from unittest import mock

import ddt
from django.conf import settings
from django.test import override_settings
from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locator import LibraryLocator, LibraryLocatorV2

from common.djangoapps.student.roles import CourseInstructorRole
from common.djangoapps.student.tests.factories import UserFactory
from openedx.core.djangoapps.content_libraries import api as library_api
from openedx.core.djangoapps.content_libraries.tests.base import ContentLibrariesRestApiTest
from openedx.core.djangoapps.xblock.api import load_block
from openedx.core.djangolib.testing.utils import skip_unless_cms
from xmodule.library_tools import LibraryToolsService
from xmodule.modulestore.tests.factories import CourseFactory, LibraryFactory
from xmodule.modulestore.tests.utils import MixedSplitTestCase


@skip_unless_cms
@ddt.ddt
class ContentLibraryToolsTest(MixedSplitTestCase, ContentLibrariesRestApiTest):
    """
    Tests for LibraryToolsService.

    Tests interaction with blockstore-based (V2) and mongo-based (V1) content libraries.
    """
    def setUp(self):
        super().setUp()
        UserFactory(is_staff=True, id=self.user_id)
        self.tools = LibraryToolsService(self.store, self.user_id)

    def test_list_available_libraries(self):
        """
        Test listing of libraries.

        Collects Only V2 Libaries if the FEATURES[ENABLE_LIBRARY_AUTHORING_MICROFRONTEND] setting is True.
        Otherwise, return all v1 and v2 libraries.
        """
        # create V1 library
        _ = LibraryFactory.create(modulestore=self.store)
        # create V2 library
        self._create_library(slug="testlib1_preview", title="Test Library 1", description="Testing XBlocks")
        all_libraries = self.tools.list_available_libraries()
        assert all_libraries
        assert len(all_libraries) == 2

        with override_settings(FEATURES={**settings.FEATURES, "ENABLE_LIBRARY_AUTHORING_MICROFRONTEND": True}):
            all_libraries = self.tools.list_available_libraries()
            assert all_libraries
            assert len(all_libraries) == 1

    @mock.patch('xmodule.modulestore.split_mongo.split.SplitMongoModuleStore.get_library_summaries')
    def test_list_available_libraries_fetch(self, mock_get_library_summaries):
        """
        Test that library list is compiled using light weight library summary objects.
        """
        _ = self.tools.list_available_libraries()
        assert mock_get_library_summaries.called

    def test_get_latest_v1_library_version(self):
        """
        Test get_v1_library_version for V1 libraries.

        Covers getting results for either string library key or LibraryLocator.
        """
        lib_key = LibraryFactory.create(modulestore=self.store).location.library_key
        # Re-load the library from the modulestore, explicitly including version information:
        lib = self.store.get_library(lib_key, remove_version=False, remove_branch=False)
        # check the result using the LibraryLocator
        assert isinstance(lib_key, LibraryLocator)
        result = self.tools.get_latest_library_version(lib_key)
        assert result
        assert result == str(lib.location.library_key.version_guid)
        # the same check for string representation of the LibraryLocator
        str_key = str(lib_key)
        result = self.tools.get_latest_library_version(str_key)
        assert result
        assert result == str(lib.location.library_key.version_guid)

    @ddt.data(
        'library-v1:Fake+Key',  # V1 library key
        'lib:Fake:V-2',         # V2 library key
        LibraryLocator.from_string('library-v1:Fake+Key'),
        LibraryLocatorV2.from_string('lib:Fake:V-2'),
    )
    def test_get_latest_library_version_no_library(self, lib_key):
        """
        Test get_latest_library_version result when the library does not exist.

        Provided lib_key's are valid V1 or V2 keys.
        """
        assert self.tools.get_latest_library_version(lib_key) is None

    def test_update_children_for_v2_lib(self):
        """
        Test update_children with V2 library as a source.
        """
        library = self._create_library(
            slug="cool-v2-lib", title="The best Library", description="Spectacular description"
        )
        self._add_block_to_library(library["id"], "unit", "unit1_id")

        course = CourseFactory.create(modulestore=self.store, user_id=self.user.id)
        CourseInstructorRole(course.id).add_users(self.user)

        content_block = self.make_block(
            "library_content",
            course,
            max_count=1,
            source_library_id=library['id']
        )
        assert len(content_block.children) == 0

        # Populate children from library
        self.tools.trigger_library_sync(content_block, library_version=None)

        # The updates happen in a Celery task, so this particular content_block instance is no updated.
        # We must re-instantiate it from modulstore in order to see the updated children list.
        content_block = self.store.get_item(content_block.location)

        assert len(content_block.children) == 1

    def test_update_children_for_v2_lib_recursive(self):
        """
        Test update_children for a V2 library containing a unit.

        Ensures that _import_from_blockstore works on nested blocks.
        """
        # Create a blockstore content library
        library = self._create_library(slug="testlib1_import", title="A Test Library", description="Testing XBlocks")
        # Create a unit block with an HTML block in it.
        unit_block_id = self._add_block_to_library(library["id"], "unit", "unit1")["id"]
        html_block_id = self._add_block_to_library(library["id"], "html", "html1", parent_block=unit_block_id)["id"]
        html_block = load_block(UsageKey.from_string(html_block_id), self.user)
        # Add assets and content to the HTML block
        self._set_library_block_asset(html_block_id, "test.txt", b"data", expect_response=200)
        self._set_library_block_olx(html_block_id, '<html><a href="/static/test.txt">Hello world</a></html>')

        # Create a modulestore course
        course = CourseFactory.create(modulestore=self.store, user_id=self.user.id)
        CourseInstructorRole(course.id).add_users(self.user)
        # Add Source from library block to the course
        lc_block = self.make_block(
            "library_content",
            course,
            user_id=self.user_id,
            max_count=1,
            source_library_id=str(library["id"]),
        )

        # Import the unit block from the library to the course
        self.tools.trigger_library_sync(lc_block, library_version=None)
        lc_block = self.store.get_item(lc_block.location)

        # Verify imported block with its children
        assert len(lc_block.children) == 1
        assert lc_block.children[0].category == 'unit'

        imported_unit_block = self.store.get_item(lc_block.children[0])
        assert len(imported_unit_block.children) == 1
        assert imported_unit_block.children[0].category == 'html'

        imported_html_block = self.store.get_item(imported_unit_block.children[0])
        assert 'Hello world' in imported_html_block.data

        # Check that assets were imported and static paths were modified after importing
        assets = library_api.get_library_block_static_asset_files(html_block.scope_ids.usage_id)
        assert len(assets) == 1
        assert assets[0].url in imported_html_block.data

        # Check that reimporting updates the target block
        self._set_library_block_olx(html_block_id, '<html><a href="/static/test.txt">Foo bar</a></html>')
        self.tools.trigger_library_sync(lc_block, library_version=None)
        lc_block = self.store.get_item(lc_block.location)

        assert len(lc_block.children) == 1
        imported_unit_block = self.store.get_item(lc_block.children[0])
        assert len(imported_unit_block.children) == 1
        imported_html_block = self.store.get_item(imported_unit_block.children[0])
        assert 'Hello world' not in imported_html_block.data
        assert 'Foo bar' in imported_html_block.data

    def test_update_children_for_v1_lib(self):
        """
        Test update_children with V1 library as a source.

        As for now, covers usage of update_children for the library content module only.
        """
        library = LibraryFactory.create(modulestore=self.store)
        self.make_block("html", library, data="Hello world from the block")
        course = CourseFactory.create(modulestore=self.store)
        content_block = self.make_block(
            "library_content",
            course,
            max_count=1,
            source_library_id=str(library.location.library_key)
        )

        assert len(content_block.children) == 0
        self.tools.trigger_library_sync(content_block, library_version=None)
        content_block = self.store.get_item(content_block.location)
        assert len(content_block.children) == 1
