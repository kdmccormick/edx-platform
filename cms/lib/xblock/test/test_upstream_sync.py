"""
Test CMS's upstream->downstream syncing system
"""
import ddt

from organizations.api import ensure_organization
from organizations.models import Organization

from cms.lib.xblock.upstream_sync import sync_from_upstream, BadUpstream, UpstreamLink, decline_sync
from common.djangoapps.student.tests.factories import UserFactory
from openedx.core.djangoapps.content_libraries import api as libs
from openedx.core.djangoapps.xblock import api as xblock
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, BlockFactory


@ddt.ddt
class UpstreamSyncTestCase(ModuleStoreTestCase):
    """
    Tests the UpstreamSyncMixin
    """

    def setUp(self):
        """
        Create a simple course with one unit.
        """
        super().setUp()
        course = CourseFactory.create()
        chapter = BlockFactory.create(category='chapter', parent=course)
        sequential = BlockFactory.create(category='sequential', parent=chapter)
        self.unit = BlockFactory.create(category='vertical', parent=sequential)

        ensure_organization("TestX")
        library = libs.create_library(
            org=Organization.objects.get(short_name="TestX"),
            slug="TestLib",
            title="Test Upstream Library",
        )
        self.upstream_key = libs.create_library_block(library.key, "html", "test-upstream").usage_key
        libs.create_library_block(library.key, "video", "video-upstream")

        upstream = xblock.load_block(self.upstream_key, self.user)
        upstream.display_name = "Upstream Title V2"
        upstream.data = "<html><body>Upstream content V2</body></html>"
        upstream.save()

    def test_sync_no_upstream(self):
        """
        Trivial case: Syncing a block with no upstream is a no-op
        """
        block = BlockFactory.create(category='html', parent=self.unit)
        block.display_name = "Block Title"
        block.data = "Block content"

        sync_from_upstream(block, self.user, apply_updates=True)

        assert block.display_name == "Block Title"
        assert block.data == "Block content"
        assert not block.upstream_display_name

    @ddt.data(
        ("not-a-key-at-all", ".*is malformed.*"),
        ("course-v1:Oops+ItsA+CourseKey", ".*is malformed.*"),
        ("block-v1:The+Wrong+KindOfUsageKey+type@html+block@nope", ".*is malformed.*"),
        ("lb:TestX:NoSuchLib:html:block-id", ".*not found in the system.*"),
        ("lb:TestX:TestLib:video:should-be-html-but-is-a-video", ".*type mismatch.*"),
        ("lb:TestX:TestLib:html:no-such-html", ".*not found in the system.*"),
    )
    @ddt.unpack
    def test_sync_bad_upstream(self, upstream, message_regex):
        """
        Syncing with a bad upstream raises BadUpstream, but doesn't affect the block
        """
        block = BlockFactory.create(category='html', parent=self.unit, upstream=upstream)
        block.display_name = "Block Title"
        block.data = "Block content"

        with self.assertRaisesRegex(BadUpstream, message_regex):
            sync_from_upstream(block, self.user, apply_updates=True)

        assert block.display_name == "Block Title"
        assert block.data == "Block content"
        assert not block.upstream_display_name

    def test_sync_not_accessible(self):
        """
        Syncing with an block that exists, but is inaccessible, raises BadUpstream
        """
        downstream = BlockFactory.create(category='html', parent=self.unit, upstream=str(self.upstream_key))
        user_who_cannot_read_upstream = UserFactory.create(username="rando", is_staff=False, is_superuser=False)
        with self.assertRaisesRegex(BadUpstream, ".*could not be loaded.*") as exc:
            sync_from_upstream(downstream, user_who_cannot_read_upstream, apply_updates=True)

    def test_sync_updates_happy_path(self):
        """
        Can we sync updates from a content library block to a linked out-of-date course block?
        """
        downstream = BlockFactory.create(category='html', parent=self.unit, upstream=str(self.upstream_key))

        # Initial sync
        sync_from_upstream(downstream, self.user, apply_updates=True)
        assert downstream.upstream_version == 2  # Library blocks start at version 2 (v1 is the empty new block)
        assert downstream.upstream_display_name == "Upstream Title V2"
        assert downstream.display_name == "Upstream Title V2"
        assert downstream.data == "<html><body>Upstream content V2</body></html>"

        # Upstream updates
        upstream = xblock.load_block(self.upstream_key, self.user)
        upstream.display_name = "Upstream Title V3"
        upstream.data = "<html><body>Upstream content V3</body></html>"
        upstream.save()

        # Follow-up sync. Assert that updates are pulled into downstream.
        sync_from_upstream(downstream, self.user, apply_updates=True)
        assert downstream.upstream_version == 3
        assert downstream.upstream_display_name == "Upstream Title V3"
        assert downstream.display_name == "Upstream Title V3"
        assert downstream.data == "<html><body>Upstream content V3</body></html>"

    def test_sync_updates_to_modified_content(self):
        """
        If we sync to modified content, will it preserve customizable fields, but overwrite the rest?
        """
        downstream = BlockFactory.create(category='html', parent=self.unit, upstream=str(self.upstream_key))

        # Initial sync
        sync_from_upstream(downstream, self.user, apply_updates=True)
        assert downstream.upstream_display_name == "Upstream Title V2"
        assert downstream.display_name == "Upstream Title V2"
        assert downstream.data == "<html><body>Upstream content V2</body></html>"

        # Upstream updates
        upstream = xblock.load_block(self.upstream_key, self.user)
        upstream.display_name = "Upstream Title V3"
        upstream.data = "<html><body>Upstream content V3</body></html>"
        upstream.save()

        # Downstream modifications
        downstream.display_name = "Downstream Title Override"  # "safe" customization
        downstream.data = "Downstream content override"  # "unsafe" override
        downstream.save()

        # Follow-up sync. Assert that updates are pulled into downstream, but customizations are saved.
        sync_from_upstream(downstream, self.user, apply_updates=True)
        assert downstream.upstream_display_name == "Upstream Title V3"
        assert downstream.display_name == "Downstream Title Override"  # "safe" customization survives
        assert downstream.data == "<html><body>Upstream content V3</body></html>"  # "unsafe" override is gone

    # For the Content Libraries Relaunch Beta, we do not yet need to support this edge case.
    # See "PRESERVING DOWNSTREAM CUSTOMIZATIONS and RESTORING UPSTREAM DEFAULTS" in cms/lib/xblock/upstream_sync.py.
    #
    #   def test_sync_to_downstream_with_subtle_customization(self):
    #       """
    #       Edge case: If our downstream customizes a field, but then the upstream is changed to match the
    #                  customization do we still remember that the downstream field is customized? That is,
    #                  if the upstream later changes again, do we retain the downstream customization (rather than
    #                  following the upstream update?)
    #       """
    #       # Start with an uncustomized downstream block.
    #       downstream = BlockFactory.create(category='html', parent=self.unit, upstream=str(self.upstream_key))
    #       sync_from_upstream(downstream, self.user, apply_updates=True)
    #       assert downstream.downstream_customized == []
    #       assert downstream.display_name == downstream.upstream_display_name == "Upstream Title V2"
    #
    #       # Then, customize our downstream title.
    #       downstream.display_name = "Title V3"
    #       downstream.save()
    #       assert downstream.downstream_customized == ["display_name"]
    #
    #       # Syncing should retain the customization.
    #       sync_from_upstream(downstream, self.user, apply_updates=True)
    #       assert downstream.upstream_version == 2
    #       assert downstream.upstream_display_name == "Upstream Title V2"
    #       assert downstream.display_name == "Title V3"
    #
    #       # Whoa, look at that, the upstream has updated itself to the exact same title...
    #       upstream = xblock.load_block(self.upstream_key, self.user)
    #       upstream.display_name = "Title V3"
    #       upstream.save()
    #
    #       # ...which is reflected when we sync.
    #       sync_from_upstream(downstream, self.user, apply_updates=True)
    #       assert downstream.upstream_version == 3
    #       assert downstream.upstream_display_name == downstream.display_name == "Title V3"
    #
    #       # But! Our downstream knows that its title is still customized.
    #       assert downstream.downstream_customized == ["display_name"]
    #       # So, if the upstream title changes again...
    #       upstream.display_name = "Title V4"
    #       upstream.save()
    #
    #       # ...then the downstream title should remain put.
    #       sync_from_upstream(downstream, self.user, apply_updates=True)
    #       assert downstream.upstream_version == 4
    #       assert downstream.upstream_display_name == "Title V4"
    #       assert downstream.display_name == "Title V3"
    #
    #       # Finally, if we "de-customize" the display_name field, then it should go back to syncing normally.
    #       downstream.downstream_customized = []
    #       upstream.display_name = "Title V5"
    #       upstream.save()
    #       sync_from_upstream(downstream, self.user, apply_updates=True)
    #       assert downstream.upstream_version == 5
    #       assert downstream.upstream_display_name == downstream.display_name == "Title V5"

    def test_sync_without_applying_updates(self):
        """
        Can we sync *defaults* (not updates) from a content library block to a linked out-of-date course block?
        """
        # Initial state: Block is linked to upstream, but with some out-of-date fields, potentially
        # from an import or a copy-paste operation.
        downstream = BlockFactory.create(category='html', parent=self.unit, upstream=str(self.upstream_key))
        assert not downstream.upstream_display_name
        downstream.display_name = "Title V1"
        downstream.data = "Content V1"

        # Sync, but without applying updates
        sync_from_upstream(downstream, self.user, apply_updates=False)

        assert downstream.upstream_display_name == "Upstream Title V2"
        assert downstream.display_name == "Title V1"
        assert downstream.data == "Content V1"

    def test_prompt_and_decline_sync(self):
        """
        Is the user prompted for sync when it's available? Does declining remove the prompt until a new sync is ready?
        """
        # Initial conditions (pre-sync)
        downstream = BlockFactory.create(category='html', parent=self.unit, upstream=str(self.upstream_key))
        link = UpstreamLink.fetch_for_block(downstream)
        assert link.version_synced is None
        assert link.version_declined is None
        assert link.version_available == 2  # Library block with content starts at version 2
        assert link.prompt_sync is True

        # Initial sync to V2
        sync_from_upstream(downstream, self.user, apply_updates=True)
        link = UpstreamLink.fetch_for_block(downstream)
        assert link.version_synced == 2
        assert link.version_declined is None
        assert link.version_available == 2
        assert link.prompt_sync is False

        # Upstream updated to V3
        upstream = xblock.load_block(self.upstream_key, self.user)
        upstream.data = "<html><body>Upstream content V3</body></html>"
        upstream.save()
        link = UpstreamLink.fetch_for_block(downstream)
        assert link.version_synced == 2
        assert link.version_declined is None
        assert link.version_available == 3
        assert link.prompt_sync is True

        # Decline to sync to V3 -- prompt_sync becomes False.
        decline_sync(downstream)
        link = UpstreamLink.fetch_for_block(downstream)
        assert link.version_synced == 2
        assert link.version_declined == 3
        assert link.version_available == 3
        assert link.prompt_sync is False

        # Upstream updated to V4 -- prompt_sync becomes True again.
        upstream = xblock.load_block(self.upstream_key, self.user)
        upstream.data = "<html><body>Upstream content V4</body></html>"
        upstream.save()
        link = UpstreamLink.fetch_for_block(downstream)
        assert link.version_synced == 2
        assert link.version_declined == 3
        assert link.version_available == 4
        assert link.prompt_sync is True
