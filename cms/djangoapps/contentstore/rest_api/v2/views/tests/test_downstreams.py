"""
Unit tests for downstream/sync views.
"""
from unittest.mock import patch

import ddt

from cms.lib.xblock.upstream_sync import UpstreamLink, BadUpstream
from common.djangoapps.student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, BlockFactory


MOCK_UPSTREAM_REF = "mock-upstream-ref"
MOCK_UPSTREAM_ERROR = "your LibraryGPT subscription has expired"


def _fetch_upstream_link_good_and_syncable(downstream):
    return UpstreamLink(
        upstream_ref=downstream.upstream,
        version_synced=downstream.upstream_version,
        version_available=downstream.upstream_version + 1,
        version_declined=downstream.upstream_version_declined,
        error_message=None,

    )


def _fetch_upstream_link_bad(_downstream):
    raise BadUpstream(MOCK_UPSTREAM_ERROR)


@ddt.ddt
class DownstreamViewTests(SharedModuleStoreTestCase):
    """
    Tests for downstream block detail view.
    """

    def setUp(self):
        """
        Create a simple course with one unit and two videos, one of which is linked to an "upstream".
        """
        super().setUp()
        course = CourseFactory.create()
        chapter = BlockFactory.create(category='chapter', parent=course)
        sequential = BlockFactory.create(category='sequential', parent=chapter)
        unit = BlockFactory.create(category='vertical', parent=sequential)
        self.regular_video_key = BlockFactory.create(category='video', parent=unit).usage_key
        self.downstream_video_key = BlockFactory.create(
            category='video', parent=unit, upstream=MOCK_UPSTREAM_REF, upstream_version=123,
        ).usage_key
        self.fake_video_key = course.id.make_usage_key("video", "NoSuchVideo")
        self.superuser = UserFactory(username="superuser", password="password", is_staff=True, is_superuser=True)
        self.learner = UserFactory(username="learner", password="password")

    @patch.object(UpstreamLink, "fetch_for_block", _fetch_upstream_link_good_and_syncable)
    def test_200_good_upstream(self):
        """
        Does the happy path work?
        """
        self.client.login(username="superuser", password="password")
        response = self.client.get(f"/api/contentstore/v2/downstreams/{self.downstream_video_key}")
        assert response.status_code == 200
        assert response.data['upstream_ref'] == MOCK_UPSTREAM_REF
        assert response.data['error_message'] is None
        assert response.data['prompt_sync'] is True

    @patch.object(UpstreamLink, "fetch_for_block", _fetch_upstream_link_bad)
    def test_200_bad_upstream(self):
        """
        If the upstream link is broken, do we still return 200, but with an error message in body?
        """
        self.client.login(username="superuser", password="password")
        response = self.client.get(f"/api/contentstore/v2/downstreams/{self.downstream_video_key}")
        assert response.status_code == 200
        assert response.data['upstream_ref'] == MOCK_UPSTREAM_REF
        assert response.data['error_message'] == MOCK_UPSTREAM_ERROR
        assert response.data['prompt_sync'] is False

    def test_200_no_upstream(self):
        """
        @@TODO change this to 404 (test_404_no_upstream)
        """
        self.client.login(username="superuser", password="password")
        response = self.client.get(f"/api/contentstore/v2/downstreams/{self.regular_video_key}")
        assert response.status_code == 200
        assert response.data is None

    def test_404_downstream_not_found(self):
        """
        Do we raise 404 if the specified downstream block could not be loaded?
        """
        self.client.login(username="superuser", password="password")
        response = self.client.get(f"/api/contentstore/v2/downstreams/{self.fake_video_key}")
        assert response.status_code == 404
        assert "not found" in response.data["developer_message"]
