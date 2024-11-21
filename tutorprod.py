from lms.envs.common import *

del ALTERNATE_ENV_TASKS
del ALTERNATE_QUEUES
del ALTERNATE_QUEUE_ENVS
del AUTH_TOKENS
del AWS_BUCKET_ACL
del AWS_DEFAULT_ACL
del BOOK_URL
del BROKER_CONNECTION_TIMEOUT
del BROKER_HEARTBEAT
del BROKER_HEARTBEAT_CHECKRATE
del BROKER_POOL_LIMIT
del BROKER_TRANSPORT_OPTIONS
del BROKER_URL
del BROKER_USE_SSL
del BULK_EMAIL_SEND_USING_EDX_ACE
del CELERYD_PREFETCH_MULTIPLIER
del CELERY_RESULT_BACKEND
del CMS_ROOT_URL
del CONFIG_FILE
del CORS_ALLOW_CREDENTIALS
del CORS_ALLOW_INSECURE
del CORS_ORIGIN_ALLOW_ALL
del CORS_ORIGIN_WHITELIST
del DASHBOARD_COURSE_LIMIT
del DEFAULT_ENTERPRISE_API_URL
del DEFAULT_ENTERPRISE_CONSENT_API_URL
del DJANGO_REDIS_IGNORE_EXCEPTIONS
del EMAIL_FILE_PATH
del ENABLE_REQUIRE_THIRD_PARTY_AUTH
del ENTITLEMENTS_EXPIRATION_ROUTING_KEY
del ENV_CELERY_QUEUES
del ENV_FEATURES
del ENV_TOKENS
del EXPLICIT_QUEUES
del HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS
del KEYS_WITH_MERGED_VALUES
del MEILISEARCH_API_KEY
del MEILISEARCH_ENABLED
del MEILISEARCH_INDEX_PREFIX
del MONGODB_LOG
del OAUTH_ENFORCE_CLIENT_SECURE
del OAUTH_EXPIRE_DELTA
del OAUTH_EXPIRE_DELTA_PUBLIC
del OAUTH_OIDC_ISSUER
del OPENEDX_LEARNING
del ORA2_FILEUPLOAD_BACKEND
del ORA2_FILEUPLOAD_CACHE_NAME
del ORA2_FILEUPLOAD_ROOT
del PREVIEW_DOMAIN
del PYTHON_LIB_FILENAME
del REGISTRATION_CODE_LENGTH
del REVISION_CONFIG
del REVISION_CONFIG_FILE
del SESSION_INACTIVITY_TIMEOUT_IN_SECONDS
del SOCIAL_AUTH_LTI_CONSUMER_SECRETS
del SOCIAL_AUTH_PIPELINE_TIMEOUT
del SSL_AUTH_DN_FORMAT_STRING
del SSL_AUTH_EMAIL_DOMAIN
del THIRD_PARTY_AUTH_CUSTOM_AUTH_FORMS
del THIRD_PARTY_AUTH_OLD_CONFIG
ALLOWED_HOSTS = []
API_ACCESS_FROM_EMAIL = "api-requests@example.com"
API_ACCESS_MANAGER_EMAIL = "api-access@example.com"
AUTHENTICATION_BACKENDS = [
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
    "bridgekeeper.backends.RulePermissionBackend",
]
AUTHN_MICROFRONTEND_DOMAIN = None
AUTHN_MICROFRONTEND_URL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = "SET-ME-PLEASE (ex. bucket-name.s3.amazonaws.com)"
AWS_STORAGE_BUCKET_NAME = "SET-ME-PLEASE (ex. bucket-name)"
BRANCH_IO_KEY = ""
BUGS_EMAIL = "bugs@example.com"
BULK_EMAIL_DEFAULT_FROM_EMAIL = "no-reply@example.com"
CACHES = {
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "KEY_FUNCTION": "common.djangoapps.util.memcache.safe_key",
        "LOCATION": ["localhost:11211"],
        "TIMEOUT": "604800",
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "use_pooling": True,
            "connect_timeout": 0.5,
        },
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "KEY_FUNCTION": "common.djangoapps.util.memcache.safe_key",
        "LOCATION": ["localhost:11211"],
        "TIMEOUT": "7200",
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "use_pooling": True,
            "connect_timeout": 0.5,
        },
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "KEY_FUNCTION": "common.djangoapps.util.memcache.safe_key",
        "LOCATION": ["localhost:11211"],
        "TIMEOUT": 300,
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "use_pooling": True,
            "connect_timeout": 0.5,
        },
    },
    "staticfiles": {
        "KEY_FUNCTION": "common.djangoapps.util.memcache.safe_key",
        "LOCATION": ["localhost:11211"],
        "KEY_PREFIX": "staticfiles_general",
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "use_pooling": True,
            "connect_timeout": 0.5,
        },
    },
    "default": {
        "VERSION": "1",
        "KEY_FUNCTION": "common.djangoapps.util.memcache.safe_key",
        "LOCATION": ["localhost:11211"],
        "KEY_PREFIX": "default",
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "use_pooling": True,
            "connect_timeout": 0.5,
        },
    },
    "configuration": {
        "KEY_FUNCTION": "common.djangoapps.util.memcache.safe_key",
        "LOCATION": ["localhost:11211"],
        "KEY_PREFIX": "configuration",
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "use_pooling": True,
            "connect_timeout": 0.5,
        },
    },
    "general": {
        "KEY_FUNCTION": "common.djangoapps.util.memcache.safe_key",
        "LOCATION": ["localhost:11211"],
        "KEY_PREFIX": "general",
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "OPTIONS": {
            "no_delay": True,
            "ignore_exc": True,
            "use_pooling": True,
            "connect_timeout": 0.5,
        },
    },
}
CC_MERCHANT_NAME = {
    "@@PYREF": "gettext_lazy",
    "@@MODULE": "django.contrib.translation.utils",
    "@@ARGS": ["Your Platform Name Here"],
}
CELERYBEAT_SCHEDULE = {}
CELERY_BROKER_HOSTNAME = "localhost"
CELERY_BROKER_PASSWORD = "celery"
CELERY_BROKER_TRANSPORT = "amqp"
CELERY_BROKER_USER = "celery"
CELERY_BROKER_VHOST = ""
del CELERY_QUEUES["edx.cms.core.default"]
CERT_QUEUE = "certificates"
CHAT_COMPLETION_API = "https://example.com/chat/completion"
CHAT_COMPLETION_API_KEY = "i am a key"
CMS_BASE = "localhost:18010"
CODE_JAIL = {
    "python_bin": "/edx/app/edxapp/venvs/edxapp-sandbox/bin/python",
    "user": "sandbox",
    "limits": {"CPU": 1, "VMEM": 536870912, "REALTIME": 3, "PROXY": 0},
    "limit_overrides": {},
}
COMMENTS_SERVICE_KEY = "password"
COMMENTS_SERVICE_URL = "http://localhost:18080"
CONTACT_EMAIL = "info@example.com"
CONTACT_MAILING_ADDRESS = "SET-ME-PLEASE"
CONTENTSTORE["OPTIONS"] = {
    "db": "edxapp",
    "host": "localhost",
    "password": "password",
    "port": 27017,
    "user": "edxapp",
    "ssl": False,
    "auth_source": None,
}
del CONTENTSTORE["DOC_STORE_CONFIG"]["connect"]
del CONTENTSTORE["DOC_STORE_CONFIG"]["authsource"]
CONTENTSTORE["DOC_STORE_CONFIG"]["db"] = "edxapp"
CONTENTSTORE["DOC_STORE_CONFIG"]["host"] = "localhost"
CONTENTSTORE["DOC_STORE_CONFIG"]["replicaSet"] = ""
CONTENTSTORE["DOC_STORE_CONFIG"]["password"] = "password"
CONTENTSTORE["DOC_STORE_CONFIG"]["user"] = "edxapp"
CONTENTSTORE["DOC_STORE_CONFIG"]["collection"] = "modulestore"
CONTENTSTORE["DOC_STORE_CONFIG"]["socketTimeoutMS"] = 6000
CONTENTSTORE["DOC_STORE_CONFIG"]["connectTimeoutMS"] = 2000
CONTENTSTORE["DOC_STORE_CONFIG"]["auth_source"] = None
CONTENTSTORE["DOC_STORE_CONFIG"]["read_preference"] = "SECONDARY_PREFERRED"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_exists"
COURSE_CATALOG_VISIBILITY_PERMISSION = "see_exists"
COURSE_LIVE_GLOBAL_CREDENTIALS = {}
CSRF_TRUSTED_ORIGINS = []
DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "NAME": "edxapp",
        "OPTIONS": {},
        "PASSWORD": "password",
        "PORT": "3306",
        "USER": "edxapp001",
    },
    "read_replica": {
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "NAME": "edxapp",
        "OPTIONS": {},
        "PASSWORD": "password",
        "PORT": "3306",
        "USER": "edxapp001",
    },
    "student_module_history": {
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "NAME": "edxapp_csmh",
        "OPTIONS": {},
        "PASSWORD": "password",
        "PORT": "3306",
        "USER": "edxapp001",
    },
}
DATABASE_ROUTERS.insert(
    0, "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)
DATA_DIR = "/edx/var/edxapp/data"
DEFAULT_EMAIL_LOGO_URL = "https://edx-cdn.org/v3/default/logo.png"
DEFAULT_FEEDBACK_EMAIL = "feedback@example.com"
DEFAULT_FROM_EMAIL = "registration@example.com"
del DOC_STORE_CONFIG["connect"]
del DOC_STORE_CONFIG["authsource"]
DOC_STORE_CONFIG["db"] = "edxapp"
DOC_STORE_CONFIG["host"] = "localhost"
DOC_STORE_CONFIG["replicaSet"] = ""
DOC_STORE_CONFIG["password"] = "password"
DOC_STORE_CONFIG["user"] = "edxapp"
DOC_STORE_CONFIG["collection"] = "modulestore"
DOC_STORE_CONFIG["socketTimeoutMS"] = 6000
DOC_STORE_CONFIG["connectTimeoutMS"] = 2000
DOC_STORE_CONFIG["auth_source"] = None
DOC_STORE_CONFIG["read_preference"] = "SECONDARY_PREFERRED"
EDX_API_KEY = "PUT_YOUR_API_KEY_HERE"
ELASTIC_SEARCH_CONFIG = [{"use_ssl": False, "host": "localhost", "port": 9200}]
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
ENABLE_COMPREHENSIVE_THEMING = False
ENABLE_MFE_CONFIG_API = False
ENTERPRISE_API_URL = "https://localhost:18000/enterprise/api/v1"
ENTERPRISE_CONSENT_API_URL = "https://localhost:18000/consent/api/v1/"
ENTERPRISE_ENROLLMENT_API_URL = "https://localhost:18000/api/enrollment/v1/"
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS = [
    "gender",
    "mailing_address",
    "age",
    "year_of_birth",
    "goals",
    "level_of_education",
]
ENTERPRISE_PUBLIC_ENROLLMENT_API_URL = "https://localhost:18000/api/enrollment/v1/"
FACEBOOK_API_VERSION = "v2.1"
FACEBOOK_APP_ID = "FACEBOOK_APP_ID"
FACEBOOK_APP_SECRET = "FACEBOOK_APP_SECRET"
del FEATURES["PREVIEW_LMS_BASE"]
del FEATURES["ENABLE_COMBINED_LOGIN_REGISTRATION"]
del FEATURES["ENABLE_LEARNER_RECORDS"]
FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
FEATURES["ENABLE_OAUTH2_PROVIDER"] = False
FEATURES["ENABLE_CORS_HEADERS"] = False
FEATURES["ENABLE_THIRD_PARTY_AUTH"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = True
FEATURES["ENABLE_MOBILE_REST_API"] = False
FEATURES["MILESTONES_APP"] = False
FEATURES["ENABLE_PREREQUISITE_COURSES"] = False
FEATURES["ENABLE_COURSEWARE_SEARCH"] = False
FEATURES["ENABLE_DASHBOARD_SEARCH"] = False
FEATURES["CERTIFICATES_HTML_VIEW"] = False
FEATURES["ENABLE_COURSE_DISCOVERY"] = False
FEATURES["ENABLE_CSMH_EXTENDED"] = True
FEATURES["ENABLE_AUTHN_MICROFRONTEND"] = False
FEATURES["ENABLE_GRADE_DOWNLOADS"] = False
FIELD_OVERRIDE_PROVIDERS = []
FILE_UPLOAD_STORAGE_BUCKET_NAME = "SET-ME-PLEASE (ex. bucket-name)"
GOOGLE_ANALYTICS_LINKEDIN = "GOOGLE_ANALYTICS_LINKEDIN_DUMMY"
GOOGLE_SITE_VERIFICATION_ID = ""
GRADES_DOWNLOAD = {
    "STORAGE_CLASS": "django.core.files.storage.FileSystemStorage",
    "STORAGE_KWARGS": {"location": "/tmp/edx-s3/grades"},
    "STORAGE_TYPE": None,
    "BUCKET": None,
    "ROOT_PATH": None,
}
HTTPS = "on"
IDA_LOGOUT_URI_LIST = []
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop(0)
INSTALLED_APPS.insert(0, "django.contrib.auth")
INSTALLED_APPS.insert(0, "django.contrib.contenttypes")
INSTALLED_APPS.insert(0, "django.contrib.humanize")
INSTALLED_APPS.insert(0, "django.contrib.messages")
INSTALLED_APPS.insert(0, "django.contrib.redirects")
INSTALLED_APPS.insert(0, "django.contrib.sessions")
INSTALLED_APPS.insert(0, "django.contrib.sites")
INSTALLED_APPS.insert(
    0, "openedx.core.djangoapps.staticfiles.apps.EdxPlatformStaticFilesConfig"
)
INSTALLED_APPS.insert(0, "django_celery_results")
INSTALLED_APPS.insert(
    0, "openedx.core.djangoapps.common_initialization.apps.CommonInitializationConfig"
)
INSTALLED_APPS.insert(
    0, "lms.djangoapps.lms_initialization.apps.LMSInitializationConfig"
)
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.common_views")
INSTALLED_APPS.insert(0, "simple_history")
INSTALLED_APPS.insert(0, "config_models")
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.config_model_utils")
INSTALLED_APPS.insert(0, "waffle")
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.service_status")
INSTALLED_APPS.insert(0, "common.djangoapps.status")
INSTALLED_APPS.insert(0, "common.djangoapps.edxmako.apps.EdxMakoConfig")
INSTALLED_APPS.insert(0, "pipeline")
INSTALLED_APPS.insert(0, "common.djangoapps.static_replace")
INSTALLED_APPS.insert(0, "webpack_loader")
INSTALLED_APPS.insert(0, "web_fragments")
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.plugin_api")
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.contentserver")
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.site_configuration")
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.video_config")
INSTALLED_APPS.insert(0, "openedx.core.djangoapps.video_pipeline")
INSTALLED_APPS.insert(0, "lms.djangoapps.courseware")
INSTALLED_APPS.insert(0, "lms.djangoapps.coursewarehistoryextended")
JWT_AUTH["JWT_SECRET_KEY"] = "dev key"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = None
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = None
JWT_AUTH["JWT_ISSUER"] = "http://127.0.0.1:8000/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "change-me"
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://127.0.0.1:8000/oauth2",
        "AUDIENCE": "change-me",
        "SECRET_KEY": "dev key",
    }
]
LEARNING_MICROFRONTEND_URL = None
LMS_BASE = "localhost:18000"
LMS_INTERNAL_ROOT_URL = "https://localhost:18000"
LMS_ROOT_URL = "https://localhost:18000"
LOGGING = {}
LOGIN_REDIRECT_WHITELIST = []
LOG_DIR = "/edx/var/log/edx"
MAINTENANCE_BANNER_TEXT = "Sample banner message"
MEDIA_ROOT = "/edx/var/edxapp/media/"
MFE_CONFIG = {}
MFE_CONFIG_API_CACHE_TIMEOUT = 300
MOBILE_STORE_ACE_URLS = {
    "google": "https://play.google.com/store/apps/details?id=org.edx.mobile",
    "apple": "https://itunes.apple.com/us/app/edx/id945480667?mt=8",
}
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
                        "db": "edxapp",
                        "host": "localhost",
                        "replicaSet": "",
                        "password": "password",
                        "port": 27017,
                        "user": "edxapp",
                        "collection": "modulestore",
                        "ssl": False,
                        "socketTimeoutMS": 6000,
                        "connectTimeoutMS": 2000,
                        "auth_source": None,
                        "read_preference": "SECONDARY_PREFERRED",
                    },
                    "OPTIONS": {
                        "default_class": "xmodule.hidden_block.HiddenBlock",
                        "fs_root": {
                            "@@PYREF": "TODO_FillInThisLambda",
                            "@@KWARGS": {
                                "hint": "'fs_root': lambda settings: settings.DATA_DIR,"
                            },
                        },
                        "render_template": "common.djangoapps.edxmako.shortcuts.render_to_string",
                    },
                },
                {
                    "NAME": "draft",
                    "ENGINE": "xmodule.modulestore.mongo.DraftMongoModuleStore",
                    "DOC_STORE_CONFIG": {
                        "db": "edxapp",
                        "host": "localhost",
                        "replicaSet": "",
                        "password": "password",
                        "port": 27017,
                        "user": "edxapp",
                        "collection": "modulestore",
                        "ssl": False,
                        "socketTimeoutMS": 6000,
                        "connectTimeoutMS": 2000,
                        "auth_source": None,
                        "read_preference": "SECONDARY_PREFERRED",
                    },
                    "OPTIONS": {
                        "default_class": "xmodule.hidden_block.HiddenBlock",
                        "fs_root": {
                            "@@PYREF": "TODO_FillInThisLambda",
                            "@@KWARGS": {
                                "hint": "'fs_root': lambda settings: settings.DATA_DIR,"
                            },
                        },
                        "render_template": "common.djangoapps.edxmako.shortcuts.render_to_string",
                    },
                },
            ],
        },
    }
}
MODULESTORE_FIELD_OVERRIDE_PROVIDERS = [
    "openedx.features.content_type_gating.field_override.ContentTypeGatingFieldOverride"
]
OAUTH_ENFORCE_SECURE = True
OPENAPI_CACHE_TIMEOUT = 0
PAYMENT_SUPPORT_EMAIL = "billing@example.com"
PLATFORM_NAME = {
    "@@PYREF": "gettext_lazy",
    "@@MODULE": "django.contrib.translation.utils",
    "@@ARGS": ["Your Platform Name Here"],
}
PRESS_EMAIL = "press@example.com"
PROFILE_IMAGE_BACKEND["options"]["location"] = "/edx/var/edxapp/media/profile-images/"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "required"
SEARCH_ENGINE = None
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = False
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = True
SECRET_KEY = "dev key"
SECURE_PROXY_SSL_HEADER = None
SERVER_EMAIL = "devops@example.com"
SESSION_COOKIE_DOMAIN = ""
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SETTINGS_MODULE = "lms.envs.common"
SHARED_COOKIE_DOMAIN = ""
SILENCED_SYSTEM_CHECKS = []
SITE_ID = 1
SITE_NAME = "localhost"
SOCIAL_MEDIA_FOOTER_ACE_URLS = {
    "reddit": "http://www.reddit.com/r/edx",
    "twitter": "https://twitter.com/edXOnline",
    "linkedin": "http://www.linkedin.com/company/edx",
    "facebook": "http://www.facebook.com/EdxOnline",
}
SOFTWARE_SECURE_VERIFICATION_ROUTING_KEY = "edx.lms.core.default"
STATIC_ROOT_BASE = "/edx/var/edxapp/staticfiles"
STATIC_URL_BASE = "/static/"
TECH_SUPPORT_EMAIL = "technical@example.com"
UNIVERSITY_EMAIL = "university@example.com"
VIDEO_CDN_URL = {"EXAMPLE_COUNTRY_CODE": "http://example.com/edx/video?s3_url="}
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"] = {"location": "/edx/var/edxapp/media/"}
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"] = {"location": "/edx/var/edxapp/media/"}
XBLOCK_FIELD_DATA_WRAPPERS = []
XBLOCK_SETTINGS = {}
XQUEUE_INTERFACE = {
    "url": "http://localhost:18040",
    "basic_auth": ["edx", "edx"],
    "django_auth": {"username": "lms", "password": "password"},
}
X_FRAME_OPTIONS = "DENY"
ZENDESK_API_KEY = ""
ZENDESK_USER = ""
