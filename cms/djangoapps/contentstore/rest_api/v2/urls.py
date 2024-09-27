"""Contenstore API v2 URLs."""

from django.conf import settings
from django.urls import path, re_path

from cms.djangoapps.contentstore.rest_api.v2.views import (
    HomePageCoursesViewV2,
    UpstreamLinkView,
    SyncFromUpstreamView,
)

app_name = "v2"

urlpatterns = [
    path(
        "home/courses",
        HomePageCoursesViewV2.as_view(),
        name="courses",
    ),
    re_path(
        fr'^downstreams/{settings.USAGE_KEY_PATTERN}/link$',
        UpstreamLinkView.as_view(),
        name="upstream_link"
    ),
    re_path(
        fr'^downstreams/{settings.USAGE_KEY_PATTERN}/sync$',
        SyncFromUpstreamView.as_view(),
        name="sync_from_upstream"
    ),
]
