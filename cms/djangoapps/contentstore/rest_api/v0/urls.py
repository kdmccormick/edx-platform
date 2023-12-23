""" Contenstore API v0 URLs. """

from django.conf import settings
from django.urls import path, re_path

from openedx.core.constants import COURSE_ID_PATTERN

from .views import (
    AdvancedCourseSettingsView,
    CourseTabListView,
    CourseTabReorderView,
    CourseTabSettingsView,
    assets,
    authoring_videos,
    transcripts,
    xblock,
)

app_name = "v0"

VIDEO_ID_PATTERN = r'(?P<edx_video_id>[-\w]+)'

urlpatterns = [
    re_path(
        fr"^advanced_settings/{COURSE_ID_PATTERN}$",
        AdvancedCourseSettingsView.as_view(),
        name="course_advanced_settings",
    ),
    re_path(
        fr"^tabs/{COURSE_ID_PATTERN}$",
        CourseTabListView.as_view(),
        name="course_tab_list",
    ),
    re_path(
        fr"^tabs/{COURSE_ID_PATTERN}/settings$",
        CourseTabSettingsView.as_view(),
        name="course_tab_settings",
    ),
    re_path(
        fr"^tabs/{COURSE_ID_PATTERN}/reorder$",
        CourseTabReorderView.as_view(),
        name="course_tab_reorder",
    ),

    # Authoring API
    re_path(
        fr'^file_assets/{settings.COURSE_ID_PATTERN}$',
        assets.AssetsCreateRetrieveView.as_view(), name='cms_api_create_retrieve_assets'
    ),
    re_path(
        fr'^file_assets/{settings.COURSE_ID_PATTERN}/{settings.ASSET_KEY_PATTERN}$',
        assets.AssetsUpdateDestroyView.as_view(), name='cms_api_update_destroy_assets'
    ),
    re_path(
        fr'^videos/encodings/{settings.COURSE_ID_PATTERN}$',
        authoring_videos.VideoEncodingsDownloadView.as_view(), name='cms_api_videos_encodings'
    ),
    path(
        'videos/features',
        authoring_videos.VideoFeaturesView.as_view(), name='cms_api_videos_features'
    ),
    re_path(
        fr'^videos/images/{settings.COURSE_ID_PATTERN}/{VIDEO_ID_PATTERN}$',
        authoring_videos.VideoImagesView.as_view(), name='cms_api_videos_images'
    ),
    re_path(
        fr'^videos/uploads/{settings.COURSE_ID_PATTERN}$',
        authoring_videos.VideosCreateUploadView.as_view(), name='cms_api_create_videos_upload'
    ),
    re_path(
        fr'^videos/uploads/{settings.COURSE_ID_PATTERN}/{VIDEO_ID_PATTERN}$',
        authoring_videos.VideosUploadsView.as_view(), name='cms_api_videos_uploads'
    ),
    re_path(
        fr'^video_transcripts/{settings.COURSE_ID_PATTERN}$',
        transcripts.TranscriptView.as_view(), name='cms_api_video_transcripts'
    ),
    re_path(
        fr'^xblock/{settings.COURSE_ID_PATTERN}$',
        xblock.XblockCreateView.as_view(), name='cms_api_create_xblock'
    ),
    re_path(
        fr'^xblock/{settings.COURSE_ID_PATTERN}/{settings.USAGE_KEY_PATTERN}$',
        xblock.XblockView.as_view(), name='cms_api_xblock'
    ),
]
