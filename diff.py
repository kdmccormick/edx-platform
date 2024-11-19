ALLOWED_HOSTS = ["local.openedx.io", "preview.local.openedx.io", "lms"]
API_ACCESS_FROM_EMAIL = "contact@local.overhang.io"
API_ACCESS_MANAGER_EMAIL = "contact@local.overhang.io"
AUTHN_MICROFRONTEND_DOMAIN = "apps.local.openedx.io/authn"
AUTHN_MICROFRONTEND_URL = "http://apps.local.openedx.io/authn"
BUGS_EMAIL = "contact@local.overhang.io"
BULK_EMAIL_DEFAULT_FROM_EMAIL = "contact@local.overhang.io"
BULK_EMAIL_SEND_USING_EDX_ACE = True
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "staticfiles": {
        "KEY_PREFIX": "staticfiles_lms",
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "staticfiles_lms",
    },
}
CODE_JAIL = {"python_bin": "nonexistingpythonbinary", "user": None}
CONTACT_MAILING_ADDRESS = "Kyle's Open edX - http://local.openedx.io"
del CONTENTSTORE["OPTIONS"]
del CONTENTSTORE["DOC_STORE_CONFIG"]["collection"]
del CONTENTSTORE["DOC_STORE_CONFIG"]["socketTimeoutMS"]
del CONTENTSTORE["DOC_STORE_CONFIG"]["connectTimeoutMS"]
del CONTENTSTORE["DOC_STORE_CONFIG"]["auth_source"]
del CONTENTSTORE["DOC_STORE_CONFIG"]["read_preference"]
CONTENTSTORE["DOC_STORE_CONFIG"]["db"] = "openedx"
CONTENTSTORE["DOC_STORE_CONFIG"]["host"] = "mongodb"
CONTENTSTORE["DOC_STORE_CONFIG"]["user"] = None
CONTENTSTORE["DOC_STORE_CONFIG"]["password"] = None
CONTENTSTORE["DOC_STORE_CONFIG"]["connect"] = False
CONTENTSTORE["DOC_STORE_CONFIG"]["authsource"] = "admin"
CONTENTSTORE["DOC_STORE_CONFIG"]["replicaSet"] = None
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_INSECURE = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ["http://local.openedx.io", "http://apps.local.openedx.io"]
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"
COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
CSRF_TRUSTED_ORIGINS = ["http://apps.local.openedx.io"]
DATABASE_ROUTERS = ["edx_django_utils.db.read_replica.ReadReplicaRouter"]
DATA_DIR = "/openedx/data/modulestore"
DEFAULT_EMAIL_LOGO_URL = "http://local.openedx.io/theming/asset/images/logo.png"
DEFAULT_FEEDBACK_EMAIL = "contact@local.overhang.io"
DEFAULT_FROM_EMAIL = "contact@local.overhang.io"
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DOC_STORE_CONFIG = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
}
ELASTIC_SEARCH_CONFIG = [{"host": "elasticsearch", "port": 9200}]
EMAIL_FILE_PATH = "/tmp/openedx/emails"
ENABLE_MFE_CONFIG_API = True
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS = [
    "goals",
    "age",
    "level_of_education",
    "year_of_birth",
    "gender",
    "mailing_address",
]
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_AUTHN_MICROFRONTEND"] = True
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}
IDA_LOGOUT_URI_LIST = ["http://studio.local.openedx.io/logout/"]
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "openedx.core.djangoapps.staticfiles.apps.EdxPlatformStaticFilesConfig",
    "django_celery_results",
    "openedx.core.djangoapps.common_initialization.apps.CommonInitializationConfig",
    "lms.djangoapps.lms_initialization.apps.LMSInitializationConfig",
    "openedx.core.djangoapps.common_views",
    "simple_history",
    "config_models",
    "openedx.core.djangoapps.config_model_utils",
    "waffle",
    "openedx.core.djangoapps.service_status",
    "common.djangoapps.status",
    "common.djangoapps.edxmako.apps.EdxMakoConfig",
    "pipeline",
    "common.djangoapps.static_replace",
    "webpack_loader",
    "web_fragments",
    "openedx.core.djangoapps.plugin_api",
    "openedx.core.djangoapps.contentserver",
    "openedx.core.djangoapps.site_configuration",
    "openedx.core.djangoapps.video_config",
    "openedx.core.djangoapps.video_pipeline",
    "lms.djangoapps.courseware",
    "common.djangoapps.student.apps.StudentConfig",
    "common.djangoapps.split_modulestore_django.apps.SplitModulestoreDjangoBackendAppConfig",
    "lms.djangoapps.static_template_view",
    "lms.djangoapps.staticbook",
    "common.djangoapps.track",
    "eventtracking.django.apps.EventTrackingConfig",
    "common.djangoapps.util",
    "lms.djangoapps.certificates.apps.CertificatesConfig",
    "lms.djangoapps.instructor_task",
    "openedx.core.djangoapps.course_groups",
    "lms.djangoapps.bulk_email",
    "lms.djangoapps.branding",
    "lms.djangoapps.course_home_api",
    "lms.djangoapps.user_tours",
    "openedx.core.djangoapps.xblock.apps.LmsXBlockAppConfig",
    "lms.djangoapps.support",
    "oauth2_provider",
    "openedx.core.djangoapps.oauth_dispatch.apps.OAuthDispatchAppConfig",
    "common.djangoapps.third_party_auth",
    "openedx.core.djangoapps.system_wide_roles",
    "openedx.core.djangoapps.auth_exchange",
    "wiki",
    "django_notify",
    "lms.djangoapps.course_wiki",
    "mptt",
    "sekizai",
    "wiki.plugins.links",
    "lms.djangoapps.course_wiki.plugins.markdownedx",
    "django.contrib.admin",
    "lms.djangoapps.debug",
    "openedx.core.djangoapps.util.apps.UtilConfig",
    "openedx.core.djangoapps.django_comment_common",
    "lms.djangoapps.edxnotes",
    "rest_framework",
    "rest_framework_jwt",
    "openedx.core.djangoapps.user_api",
    "common.djangoapps.course_modes.apps.CourseModesConfig",
    "openedx.core.djangoapps.enrollments.apps.EnrollmentsConfig",
    "common.djangoapps.entitlements.apps.EntitlementsConfig",
    "lms.djangoapps.bulk_enroll",
    "lms.djangoapps.verify_student.apps.VerifyStudentConfig",
    "openedx.core.djangoapps.dark_lang",
    "lms.djangoapps.rss_proxy",
    "openedx.core.djangoapps.embargo",
    "common.djangoapps.course_action_state",
    "django_countries",
    "lms.djangoapps.mobile_api.apps.MobileApiConfig",
    "social_django",
    "lms.djangoapps.survey.apps.SurveyConfig",
    "lms.djangoapps.lms_xblock.apps.LMSXBlockConfig",
    "submissions",
    "openassessment",
    "openassessment.assessment",
    "openassessment.fileupload",
    "openassessment.staffgrader",
    "openassessment.workflow",
    "openassessment.xblock",
    "edxval",
    "openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig",
    "openedx.core.djangoapps.content.block_structure.apps.BlockStructureConfig",
    "lms.djangoapps.course_blocks",
    "lms.djangoapps.mailing",
    "corsheaders",
    "openedx.core.djangoapps.cors_csrf",
    "lms.djangoapps.commerce.apps.CommerceConfig",
    "openedx.core.djangoapps.credit.apps.CreditConfig",
    "lms.djangoapps.teams",
    "common.djangoapps.xblock_django",
    "openedx.core.djangoapps.programs.apps.ProgramsConfig",
    "openedx.core.djangoapps.catalog",
    "sorl.thumbnail",
    "milestones",
    "lms.djangoapps.gating.apps.GatingConfig",
    "statici18n",
    "openedx.core.djangoapps.api_admin",
    "openedx.core.djangoapps.verified_track_content",
    "lms.djangoapps.learner_dashboard",
    "lms.djangoapps.badges.apps.BadgesConfig",
    "django_sites_extensions",
    "lms.djangoapps.email_marketing.apps.EmailMarketingConfig",
    "release_util",
    "rules.apps.AutodiscoverRulesConfig",
    "bridgekeeper",
    "user_tasks",
    "celery_utils",
    "openedx.core.djangoapps.crawlers",
    "common.djangoapps.database_fixups",
    "openedx.core.djangoapps.waffle_utils",
    "lms.djangoapps.course_goals.apps.CourseGoalsConfig",
    "openedx_tagging.core.tagging.apps.TaggingConfig",
    "openedx.core.djangoapps.content_tagging",
    "openedx.features.calendar_sync",
    "openedx.features.course_bookmarks",
    "openedx.features.course_experience",
    "openedx.features.enterprise_support.apps.EnterpriseSupportConfig",
    "openedx.features.learner_profile",
    "openedx.features.course_duration_limits",
    "openedx.features.content_type_gating",
    "openedx.features.discounts",
    "openedx.features.effort_estimation",
    "openedx.features.name_affirmation_api.apps.NameAffirmationApiConfig",
    "lms.djangoapps.experiments",
    "django_filters",
    "drf_yasg",
    "csrf.apps.CsrfAppConfig",
    "xss_utils",
    "openedx.core.djangoapps.heartbeat",
    "openedx.core.djangoapps.course_date_signals",
    "openedx.core.djangoapps.external_user_ids",
    "openedx.core.djangoapps.schedules",
    "openedx.core.djangoapps.content.learning_sequences.apps.LearningSequencesConfig",
    "organizations",
    "lms.djangoapps.bulk_user_retirement",
    "openedx.core.djangoapps.agreements",
    "openedx.features.survey_report",
    "edx_django_utils.user",
    "pylti1p3.contrib.django.lti1p3_tool_config",
    "edx_ace",
    "lms.djangoapps.mfe_config_api",
    "openedx.core.djangoapps.notifications",
    "openedx_events",
    "openedx_learning.apps.authoring.collections",
    "openedx_learning.apps.authoring.components",
    "openedx_learning.apps.authoring.contents",
    "openedx_learning.apps.authoring.publishing",
    "edx_sga",
    "enterprise",
    "consent",
    "integrated_channels.integrated_channel",
    "integrated_channels.degreed",
    "integrated_channels.degreed2",
    "integrated_channels.sap_success_factors",
    "integrated_channels.cornerstone",
    "integrated_channels.xapi",
    "integrated_channels.blackboard",
    "integrated_channels.canvas",
    "integrated_channels.moodle",
    "django_object_actions",
    "openedx.core.djangoapps.ace_common.apps.AceCommonConfig",
    "openedx.core.djangoapps.bookmarks.apps.BookmarksConfig",
    "openedx.core.djangoapps.content_libraries.apps.ContentLibrariesConfig",
    "openedx.core.djangoapps.course_apps.apps.CourseAppsConfig",
    "openedx.core.djangoapps.course_live.apps.CourseLiveConfig",
    "openedx.core.djangoapps.courseware_api.apps.CoursewareAPIConfig",
    "openedx.core.djangoapps.credentials.apps.CredentialsConfig",
    "lms.djangoapps.discussion.apps.DiscussionConfig",
    "openedx.core.djangoapps.discussions.apps.DiscussionsConfig",
    "lms.djangoapps.grades.apps.GradesConfig",
    "lms.djangoapps.instructor.apps.InstructorConfig",
    "openedx.core.djangoapps.password_policy.apps.PasswordPolicyConfig",
    "openedx.core.djangoapps.plugins.apps.PluginsConfig",
    "lms.djangoapps.program_enrollments.apps.ProgramEnrollmentsConfig",
    "openedx.core.djangoapps.theming.apps.ThemingConfig",
    "openedx.core.djangoapps.user_authn.apps.UserAuthnConfig",
    "openedx.core.djangoapps.zendesk_proxy.apps.ZendeskProxyConfig",
    "bulk_grades.apps.BulkGradesConfig",
    "completion.apps.CompletionAppConfig",
    "super_csv.apps.SuperCSVConfig",
    "edx_when.apps.EdxWhenConfig",
    "edx_name_affirmation.apps.EdxNameAffirmationConfig",
    "edx_proctoring.apps.EdxProctoringConfig",
    "lti_consumer.apps.LTIConsumerApp",
    "edx_toggles.apps.TogglesConfig",
    "push_notifications",
]
JWT_AUTH["JWT_SECRET_KEY"] = "o5wToOrEitfAxwP8E5U0n5zi"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = (
    '{"kid": "openedx", "kty": "RSA", "e": "AQAB", "d": "OmweNydMBC_YOib6WZM4ph76gwT9sfvYn6qFAdFRS-PiGgyJC-6YSsY2VVViGpcbXaLcnykSv6_pvQL4PW-8XLuqylKbRlQDBX1ud-IbAAaEGBmRAW2_jfR11QH4gNmiORgrHFUe-eDghvdz6DpSTpAPDSUiSPhjDluAJ4Ya6vBkul7lITj7KdruWpb6XynxqO8dmqPv5xX112DVJSOd7sb33O8B3P7i41AD26E-117oo0zJRVZHv7DKFM23eYLBubaXQ4L0TYAJSqktniv-7Fc5cmwtTm5EeefWwun4uv6D_qVhLi0wQ0lHTx4eKi4uLkYvdTdLwqSl_GdCy4ZooQ", "n": "kOvj-HTtKIpBcZfwMR9Mt1L89RqiT4wjJjUk-pipRSgYebBD1Pl9oS6jIVRfMM8HN15mHAnw0GQ-Szy1PR830Ro8IjzABMyUnV0s0U0yNoJYlquiJ-jBIXzM5Ekm5vGmfoftmDT557xZ1znRGV6iVEiwF3Ng6quBtmwfMO9lcPEHhBrrHQchdC-boPiqQZmHocy-eHUgXqnZ752t3-x0cqenIBo-3ueefxAnZAm2YnT4-v3RItDuZa5mchFUO9UL4ZpFZ7GoabddlXCsYqymXylrU13IwbS6Lh00C-7sm9_lcJTRzqVBtx2DU2KTxh1fATs1A4G89anYVbpH1Ntyfw", "p": "vctSrWpidXYVcf9RjhB1Ok_Ye2xwkK9u99YIBxu0Dh-4q79OFhYTBgLqjz1DXa0quSf92z5Xf41d2NWnd5VWktZUg4Zrqsrc2NOlXZcwbb-XD41sweC3xQL_uB8RdUswkxlW065XXDC0MZD6_hUCYIVBJSdrM8ZTlAndad0RlbM", "q": "w3lqaVa58k_S2E0ldB1BcMGcI6KyLL5T6YdSogTSyKt87cZbEtjehNoRwg2IRSr7kcbuoUMWlpeVLWWcZnuu2dHKYSg4ACyXFykZtqyKUZSe-fgyEPg1ZpL8JTIelXW-y8x5LbnXsr8tfWXL9PUVpFPbsn8KePcOP1M2_QZ3YgU", "dq": "eNYYqu-a2SjxPRdLnODs8EgvPnQ30qMBem5V7aQvrS8ddltVN2xq-hNYQO5em-t7Ql2IbJXtY8Bmzn5u1YeFyk7-3Vqga7Mk34NfyuYUR2Qpdnswb_8P-83HIzM9ZsU34gIPsu2cYnn-I_OGxnGvJDtWp5wTHD4VR54ocvfJWwU", "dp": "rOYoCHENBwKu4K3-ZtQZZyjMBwwvs68OAVsK7ybOrbs6KcPaaAZuCCDp-9mMoC8b55dGDM_LOBjZsKpaqHb0ako0rajsNqgd7q1ITW1pIeHSxMlKlYiZATINMXekGN2Jf8gqsCZ30TVRQoJYFNWg17stMKKrZ3w6MXeXLFTHKz8", "qi": "KYhS58SxpzaojYS5sfXIhLEtAja0MerYU8cDHMwHrYw6_VZ8OxKErIUp_hrE-wJwF9YaWRbUh55Ys1eEKH6aKvSK2G2tUCXR7-320uUZeh7orOiWYAYTrn9RGc2hyFpeabL-QrIy9h4nrEPJwchc2ybQsgSJfHYWuwkT2hcK8bM"}'
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = (
    '{"keys": [{"kid": "openedx", "kty": "RSA", "e": "AQAB", "n": "kOvj-HTtKIpBcZfwMR9Mt1L89RqiT4wjJjUk-pipRSgYebBD1Pl9oS6jIVRfMM8HN15mHAnw0GQ-Szy1PR830Ro8IjzABMyUnV0s0U0yNoJYlquiJ-jBIXzM5Ekm5vGmfoftmDT557xZ1znRGV6iVEiwF3Ng6quBtmwfMO9lcPEHhBrrHQchdC-boPiqQZmHocy-eHUgXqnZ752t3-x0cqenIBo-3ueefxAnZAm2YnT4-v3RItDuZa5mchFUO9UL4ZpFZ7GoabddlXCsYqymXylrU13IwbS6Lh00C-7sm9_lcJTRzqVBtx2DU2KTxh1fATs1A4G89anYVbpH1Ntyfw"}]}'
)
JWT_AUTH["JWT_ISSUER"] = "http://local.openedx.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.openedx.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "o5wToOrEitfAxwP8E5U0n5zi",
    }
]
LEARNING_MICROFRONTEND_URL = "http://apps.local.openedx.io/learning"
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": "/openedx/data/logs/all.log",
    "formatter": "standard",
}
del LOGGING["handlers"]["tracking"]["address"]
del LOGGING["handlers"]["tracking"]["facility"]
LOGGING["handlers"]["tracking"]["class"] = "logging.handlers.WatchedFileHandler"
LOGGING["handlers"]["tracking"]["filename"] = "/openedx/data/logs/tracking.log"
LOGGING["handlers"]["tracking"]["formatter"] = "standard"
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {
    "handlers": ["console"],
    "level": "WARNING",
}
LOGIN_REDIRECT_WHITELIST = ["studio.local.openedx.io", "apps.local.openedx.io"]
MEDIA_ROOT = "/openedx/media/"
MEILISEARCH_ENABLED = True
MEILISEARCH_INDEX_PREFIX = "tutor_"
MFE_CONFIG = {
    "BASE_URL": "apps.local.openedx.io",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "CREDENTIALS_BASE_URL": "",
    "DISCOVERY_API_BASE_URL": "",
    "FAVICON_URL": "http://local.openedx.io/favicon.ico",
    "INFO_EMAIL": "contact@local.overhang.io",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "http://local.openedx.io",
    "LOGIN_URL": "http://local.openedx.io/login",
    "LOGO_URL": "http://local.openedx.io/theming/asset/images/logo.png",
    "LOGO_WHITE_URL": "http://local.openedx.io/theming/asset/images/logo.png",
    "LOGO_TRADEMARK_URL": "http://local.openedx.io/theming/asset/images/logo.png",
    "LOGOUT_URL": "http://local.openedx.io/logout",
    "MARKETING_SITE_BASE_URL": "http://local.openedx.io",
    "PASSWORD_RESET_SUPPORT_LINK": "mailto:contact@local.overhang.io",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "http://local.openedx.io/login_refresh",
    "SITE_NAME": "Kyle's Open edX",
    "STUDIO_BASE_URL": "http://studio.local.openedx.io",
    "USER_INFO_COOKIE_NAME": "user-info",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
    "DISABLE_ENTERPRISE_LOGIN": True,
    "COURSE_AUTHORING_MICROFRONTEND_URL": "http://apps.local.openedx.io/authoring",
    "ENABLE_ASSETS_PAGE": "true",
    "ENABLE_HOME_PAGE_COURSE_API_V2": "true",
    "ENABLE_PROGRESS_GRAPH_SETTINGS": "true",
    "ENABLE_TAGGING_TAXONOMY_PAGES": "true",
    "LEARNING_BASE_URL": "http://apps.local.openedx.io/learning",
    "MEILISEARCH_ENABLED": True,
}
MFE_CONFIG_API_CACHE_TIMEOUT = 1
MOBILE_STORE_ACE_URLS = {}
MODULESTORE = {
    "default": {
        "ENGINE": "xmodule.modulestore.mixed.MixedModuleStore",
        "OPTIONS": {
            "mappings": {},
            "stores": [
                {
                    "NAME": "split",
                    "ENGINE": "xmodule.modulestore.split_mongo.split_draft.DraftVersioningModuleStore",
                    "DOC_STORE_CONFIG": {
                        "db": "openedx",
                        "host": "mongodb",
                        "replicaSet": None,
                        "password": None,
                        "port": 27017,
                        "user": None,
                        "collection": "modulestore",
                        "ssl": False,
                        "socketTimeoutMS": 6000,
                        "connectTimeoutMS": 2000,
                        "auth_source": None,
                        "read_preference": "SECONDARY_PREFERRED",
                        "connect": False,
                        "authsource": "admin",
                    },
                    "OPTIONS": {
                        "default_class": "xmodule.hidden_block.HiddenBlock",
                        "fs_root": "/openedx/data/modulestore",
                        "render_template": "common.djangoapps.edxmako.shortcuts.render_to_string",
                    },
                },
                {
                    "NAME": "draft",
                    "ENGINE": "xmodule.modulestore.mongo.DraftMongoModuleStore",
                    "DOC_STORE_CONFIG": {
                        "db": "openedx",
                        "host": "mongodb",
                        "replicaSet": None,
                        "password": None,
                        "port": 27017,
                        "user": None,
                        "collection": "modulestore",
                        "ssl": False,
                        "socketTimeoutMS": 6000,
                        "connectTimeoutMS": 2000,
                        "auth_source": None,
                        "read_preference": "SECONDARY_PREFERRED",
                        "connect": False,
                        "authsource": "admin",
                    },
                    "OPTIONS": {
                        "default_class": "xmodule.hidden_block.HiddenBlock",
                        "fs_root": "/openedx/data/modulestore",
                        "render_template": "common.djangoapps.edxmako.shortcuts.render_to_string",
                    },
                },
            ],
        },
    }
}
OAUTH_ENFORCE_SECURE = False
OPENEDX_LEARNING = {
    "MEDIA": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {"location": "/openedx/media-private/openedx-learning"},
    }
}
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
PAYMENT_SUPPORT_EMAIL = "contact@local.overhang.io"
PRESS_EMAIL = "contact@local.overhang.io"
PROFILE_IMAGE_BACKEND["options"]["location"] = "/openedx/media/profile-images/"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False
SERVER_EMAIL = "contact@local.overhang.io"
SESSION_COOKIE_SAMESITE = "Lax"
SETTINGS_MODULE = "lms.envs.tutor.production"
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]
SITE_ID = 2
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}
TECH_SUPPORT_EMAIL = "contact@local.overhang.io"
UNIVERSITY_EMAIL = "contact@local.overhang.io"
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"] = {"location": "/openedx/media/"}
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"] = {"location": "/openedx/media/"}
X_FRAME_OPTIONS = "SAMEORIGIN"
