ALLOWED_HOSTS = ['local.openedx.io', 'preview.local.openedx.io', 'lms']
API_ACCESS_FROM_EMAIL = 'contact@local.overhang.io'
API_ACCESS_MANAGER_EMAIL = 'contact@local.overhang.io'
AUTHN_MICROFRONTEND_DOMAIN = 'apps.local.openedx.io/authn'
AUTHN_MICROFRONTEND_URL = 'http://apps.local.openedx.io/authn'
BUGS_EMAIL = 'contact@local.overhang.io'
BULK_EMAIL_DEFAULT_FROM_EMAIL = 'contact@local.overhang.io'
BULK_EMAIL_SEND_USING_EDX_ACE = True
CACHES = {'default': {'KEY_PREFIX': 'default', 'VERSION': '1', 'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://@redis:6379/1'}, 'general': {'KEY_PREFIX': 'general', 'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://@redis:6379/1'}, 'mongo_metadata_inheritance': {'KEY_PREFIX': 'mongo_metadata_inheritance', 'TIMEOUT': 300, 'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://@redis:6379/1'}, 'configuration': {'KEY_PREFIX': 'configuration', 'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://@redis:6379/1'}, 'celery': {'KEY_PREFIX': 'celery', 'TIMEOUT': 7200, 'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://@redis:6379/1'}, 'course_structure_cache': {'KEY_PREFIX': 'course_structure', 'TIMEOUT': 604800, 'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://@redis:6379/1'}, 'ora2-storage': {'KEY_PREFIX': 'ora2-storage', 'BACKEND': 'django_redis.cache.RedisCache', 'LOCATION': 'redis://@redis:6379/1'}, 'staticfiles': {'KEY_PREFIX': 'staticfiles_lms', 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'staticfiles_lms'}}
CODE_JAIL = {'python_bin': 'nonexistingpythonbinary', 'user': None}
CONTACT_MAILING_ADDRESS = "Kyle's Open edX - http://local.openedx.io"
del CONTENTSTORE['OPTIONS']
del CONTENTSTORE['DOC_STORE_CONFIG']['collection']
del CONTENTSTORE['DOC_STORE_CONFIG']['socketTimeoutMS']
del CONTENTSTORE['DOC_STORE_CONFIG']['connectTimeoutMS']
del CONTENTSTORE['DOC_STORE_CONFIG']['auth_source']
del CONTENTSTORE['DOC_STORE_CONFIG']['read_preference']
CONTENTSTORE['DOC_STORE_CONFIG']['db'] = 'openedx'
CONTENTSTORE['DOC_STORE_CONFIG']['host'] = 'mongodb'
CONTENTSTORE['DOC_STORE_CONFIG']['user'] = None
CONTENTSTORE['DOC_STORE_CONFIG']['password'] = None
CONTENTSTORE['DOC_STORE_CONFIG']['connect'] = False
CONTENTSTORE['DOC_STORE_CONFIG']['authsource'] = 'admin'
CONTENTSTORE['DOC_STORE_CONFIG']['replicaSet'] = None
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_INSECURE = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['http://local.openedx.io', 'http://apps.local.openedx.io']
COURSE_ABOUT_VISIBILITY_PERMISSION = 'see_about_page'
COURSE_CATALOG_VISIBILITY_PERMISSION = 'see_in_catalog'
CSRF_TRUSTED_ORIGINS = ['http://apps.local.openedx.io']
DATABASE_ROUTERS = ['edx_django_utils.db.read_replica.ReadReplicaRouter']
DATA_DIR = '/openedx/data/modulestore'
DEFAULT_EMAIL_LOGO_URL = 'http://local.openedx.io/theming/asset/images/logo.png'
DEFAULT_FEEDBACK_EMAIL = 'contact@local.overhang.io'
DEFAULT_FROM_EMAIL = 'contact@local.overhang.io'
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DOC_STORE_CONFIG = {'db': 'openedx', 'host': 'mongodb', 'port': 27017, 'user': None, 'password': None, 'connect': False, 'ssl': False, 'authsource': 'admin', 'replicaSet': None}
ELASTIC_SEARCH_CONFIG = [{'host': 'elasticsearch', 'port': 9200}]
EMAIL_FILE_PATH = '/tmp/openedx/emails'
ENABLE_MFE_CONFIG_API = True
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS[2] = 'level_of_education'
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS[3] = 'year_of_birth'
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS[4] = 'gender'
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS[5] = 'mailing_address'
FEATURES['ENABLE_DISCUSSION_SERVICE'] = False
FEATURES['ENABLE_CORS_HEADERS'] = True
FEATURES['PREVENT_CONCURRENT_LOGINS'] = False
FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = True
FILE_UPLOAD_STORAGE_BUCKET_NAME = 'openedxuploads'
GRADES_DOWNLOAD = {'STORAGE_TYPE': '', 'STORAGE_KWARGS': {'base_url': '/media/grades/', 'location': '/openedx/media/grades'}}
IDA_LOGOUT_URI_LIST = ['http://studio.local.openedx.io/logout/']
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
INSTALLED_APPS.pop(0)
INSTALLED_APPS.pop()
INSTALLED_APPS.insert(0, 'django.contrib.auth')
INSTALLED_APPS.insert(0, 'django.contrib.contenttypes')
INSTALLED_APPS.insert(0, 'django.contrib.humanize')
INSTALLED_APPS.insert(0, 'django.contrib.messages')
INSTALLED_APPS.insert(0, 'django.contrib.redirects')
INSTALLED_APPS.insert(0, 'django.contrib.sessions')
INSTALLED_APPS.insert(0, 'django.contrib.sites')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.staticfiles.apps.EdxPlatformStaticFilesConfig')
INSTALLED_APPS.insert(0, 'django_celery_results')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.common_initialization.apps.CommonInitializationConfig')
INSTALLED_APPS.insert(0, 'lms.djangoapps.lms_initialization.apps.LMSInitializationConfig')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.common_views')
INSTALLED_APPS.insert(0, 'simple_history')
INSTALLED_APPS.insert(0, 'config_models')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.config_model_utils')
INSTALLED_APPS.insert(0, 'waffle')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.service_status')
INSTALLED_APPS.insert(0, 'common.djangoapps.status')
INSTALLED_APPS.insert(0, 'common.djangoapps.edxmako.apps.EdxMakoConfig')
INSTALLED_APPS.insert(0, 'pipeline')
INSTALLED_APPS.insert(0, 'common.djangoapps.static_replace')
INSTALLED_APPS.insert(0, 'webpack_loader')
INSTALLED_APPS.insert(0, 'web_fragments')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.plugin_api')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.contentserver')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.site_configuration')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.video_config')
INSTALLED_APPS.insert(0, 'openedx.core.djangoapps.video_pipeline')
INSTALLED_APPS.insert(0, 'lms.djangoapps.courseware')
JWT_AUTH['JWT_SECRET_KEY'] = 'o5wToOrEitfAxwP8E5U0n5zi'
JWT_AUTH['JWT_PRIVATE_SIGNING_JWK'] = '{"kid": "openedx", "kty": "RSA", "e": "AQAB", "d": "OmweNydMBC_YOib6WZM4ph76gwT9sfvYn6qFAdFRS-PiGgyJC-6YSsY2VVViGpcbXaLcnykSv6_pvQL4PW-8XLuqylKbRlQDBX1ud-IbAAaEGBmRAW2_jfR11QH4gNmiORgrHFUe-eDghvdz6DpSTpAPDSUiSPhjDluAJ4Ya6vBkul7lITj7KdruWpb6XynxqO8dmqPv5xX112DVJSOd7sb33O8B3P7i41AD26E-117oo0zJRVZHv7DKFM23eYLBubaXQ4L0TYAJSqktniv-7Fc5cmwtTm5EeefWwun4uv6D_qVhLi0wQ0lHTx4eKi4uLkYvdTdLwqSl_GdCy4ZooQ", "n": "kOvj-HTtKIpBcZfwMR9Mt1L89RqiT4wjJjUk-pipRSgYebBD1Pl9oS6jIVRfMM8HN15mHAnw0GQ-Szy1PR830Ro8IjzABMyUnV0s0U0yNoJYlquiJ-jBIXzM5Ekm5vGmfoftmDT557xZ1znRGV6iVEiwF3Ng6quBtmwfMO9lcPEHhBrrHQchdC-boPiqQZmHocy-eHUgXqnZ752t3-x0cqenIBo-3ueefxAnZAm2YnT4-v3RItDuZa5mchFUO9UL4ZpFZ7GoabddlXCsYqymXylrU13IwbS6Lh00C-7sm9_lcJTRzqVBtx2DU2KTxh1fATs1A4G89anYVbpH1Ntyfw", "p": "vctSrWpidXYVcf9RjhB1Ok_Ye2xwkK9u99YIBxu0Dh-4q79OFhYTBgLqjz1DXa0quSf92z5Xf41d2NWnd5VWktZUg4Zrqsrc2NOlXZcwbb-XD41sweC3xQL_uB8RdUswkxlW065XXDC0MZD6_hUCYIVBJSdrM8ZTlAndad0RlbM", "q": "w3lqaVa58k_S2E0ldB1BcMGcI6KyLL5T6YdSogTSyKt87cZbEtjehNoRwg2IRSr7kcbuoUMWlpeVLWWcZnuu2dHKYSg4ACyXFykZtqyKUZSe-fgyEPg1ZpL8JTIelXW-y8x5LbnXsr8tfWXL9PUVpFPbsn8KePcOP1M2_QZ3YgU", "dq": "eNYYqu-a2SjxPRdLnODs8EgvPnQ30qMBem5V7aQvrS8ddltVN2xq-hNYQO5em-t7Ql2IbJXtY8Bmzn5u1YeFyk7-3Vqga7Mk34NfyuYUR2Qpdnswb_8P-83HIzM9ZsU34gIPsu2cYnn-I_OGxnGvJDtWp5wTHD4VR54ocvfJWwU", "dp": "rOYoCHENBwKu4K3-ZtQZZyjMBwwvs68OAVsK7ybOrbs6KcPaaAZuCCDp-9mMoC8b55dGDM_LOBjZsKpaqHb0ako0rajsNqgd7q1ITW1pIeHSxMlKlYiZATINMXekGN2Jf8gqsCZ30TVRQoJYFNWg17stMKKrZ3w6MXeXLFTHKz8", "qi": "KYhS58SxpzaojYS5sfXIhLEtAja0MerYU8cDHMwHrYw6_VZ8OxKErIUp_hrE-wJwF9YaWRbUh55Ys1eEKH6aKvSK2G2tUCXR7-320uUZeh7orOiWYAYTrn9RGc2hyFpeabL-QrIy9h4nrEPJwchc2ybQsgSJfHYWuwkT2hcK8bM"}'
JWT_AUTH['JWT_PUBLIC_SIGNING_JWK_SET'] = '{"keys": [{"kid": "openedx", "kty": "RSA", "e": "AQAB", "n": "kOvj-HTtKIpBcZfwMR9Mt1L89RqiT4wjJjUk-pipRSgYebBD1Pl9oS6jIVRfMM8HN15mHAnw0GQ-Szy1PR830Ro8IjzABMyUnV0s0U0yNoJYlquiJ-jBIXzM5Ekm5vGmfoftmDT557xZ1znRGV6iVEiwF3Ng6quBtmwfMO9lcPEHhBrrHQchdC-boPiqQZmHocy-eHUgXqnZ752t3-x0cqenIBo-3ueefxAnZAm2YnT4-v3RItDuZa5mchFUO9UL4ZpFZ7GoabddlXCsYqymXylrU13IwbS6Lh00C-7sm9_lcJTRzqVBtx2DU2KTxh1fATs1A4G89anYVbpH1Ntyfw"}]}'
JWT_AUTH['JWT_ISSUER'] = 'http://local.openedx.io/oauth2'
JWT_AUTH['JWT_AUDIENCE'] = 'openedx'
JWT_AUTH['JWT_ISSUERS'] = [{'ISSUER': 'http://local.openedx.io/oauth2', 'AUDIENCE': 'openedx', 'SECRET_KEY': 'o5wToOrEitfAxwP8E5U0n5zi'}]
LEARNING_MICROFRONTEND_URL = 'http://apps.local.openedx.io/learning'
LOGGING['handlers']['local'] = {'class': 'logging.handlers.WatchedFileHandler', 'filename': '/openedx/data/logs/all.log', 'formatter': 'standard'}
del LOGGING['handlers']['tracking']['address']
del LOGGING['handlers']['tracking']['facility']
LOGGING['handlers']['tracking']['class'] = 'logging.handlers.WatchedFileHandler'
LOGGING['handlers']['tracking']['filename'] = '/openedx/data/logs/tracking.log'
LOGGING['handlers']['tracking']['formatter'] = 'standard'
LOGGING['loggers']['tracking']['handlers'].insert(0, 'console')
LOGGING['loggers']['tracking']['handlers'].insert(0, 'local')
LOGGING['loggers']['blockstore.apps.bundles.storage'] = {'handlers': ['console'], 'level': 'WARNING'}
LOGIN_REDIRECT_WHITELIST = ['studio.local.openedx.io', 'apps.local.openedx.io']
MEDIA_ROOT = '/openedx/media/'
MEILISEARCH_ENABLED = True
MEILISEARCH_INDEX_PREFIX = 'tutor_'
MFE_CONFIG = {'BASE_URL': 'apps.local.openedx.io', 'CSRF_TOKEN_API_PATH': '/csrf/api/v1/token', 'CREDENTIALS_BASE_URL': '', 'DISCOVERY_API_BASE_URL': '', 'FAVICON_URL': 'http://local.openedx.io/favicon.ico', 'INFO_EMAIL': 'contact@local.overhang.io', 'LANGUAGE_PREFERENCE_COOKIE_NAME': 'openedx-language-preference', 'LMS_BASE_URL': 'http://local.openedx.io', 'LOGIN_URL': 'http://local.openedx.io/login', 'LOGO_URL': 'http://local.openedx.io/theming/asset/images/logo.png', 'LOGO_WHITE_URL': 'http://local.openedx.io/theming/asset/images/logo.png', 'LOGO_TRADEMARK_URL': 'http://local.openedx.io/theming/asset/images/logo.png', 'LOGOUT_URL': 'http://local.openedx.io/logout', 'MARKETING_SITE_BASE_URL': 'http://local.openedx.io', 'PASSWORD_RESET_SUPPORT_LINK': 'mailto:contact@local.overhang.io', 'REFRESH_ACCESS_TOKEN_ENDPOINT': 'http://local.openedx.io/login_refresh', 'SITE_NAME': "Kyle's Open edX", 'STUDIO_BASE_URL': 'http://studio.local.openedx.io', 'USER_INFO_COOKIE_NAME': 'user-info', 'ACCESS_TOKEN_COOKIE_NAME': 'edx-jwt-cookie-header-payload', 'DISABLE_ENTERPRISE_LOGIN': True, 'COURSE_AUTHORING_MICROFRONTEND_URL': 'http://apps.local.openedx.io/authoring', 'ENABLE_ASSETS_PAGE': 'true', 'ENABLE_HOME_PAGE_COURSE_API_V2': 'true', 'ENABLE_PROGRESS_GRAPH_SETTINGS': 'true', 'ENABLE_TAGGING_TAXONOMY_PAGES': 'true', 'LEARNING_BASE_URL': 'http://apps.local.openedx.io/learning', 'MEILISEARCH_ENABLED': True}
MFE_CONFIG_API_CACHE_TIMEOUT = 1
MOBILE_STORE_ACE_URLS = {}
MODULESTORE = {'default': {'ENGINE': 'xmodule.modulestore.mixed.MixedModuleStore', 'OPTIONS': {'mappings': {}, 'stores': [{'NAME': 'split', 'ENGINE': 'xmodule.modulestore.split_mongo.split_draft.DraftVersioningModuleStore', 'DOC_STORE_CONFIG': {'db': 'openedx', 'host': 'mongodb', 'replicaSet': None, 'password': None, 'port': 27017, 'user': None, 'collection': 'modulestore', 'ssl': False, 'socketTimeoutMS': 6000, 'connectTimeoutMS': 2000, 'auth_source': None, 'read_preference': 'SECONDARY_PREFERRED', 'connect': False, 'authsource': 'admin'}, 'OPTIONS': {'default_class': 'xmodule.hidden_block.HiddenBlock', 'fs_root': '/openedx/data/modulestore', 'render_template': 'common.djangoapps.edxmako.shortcuts.render_to_string'}}, {'NAME': 'draft', 'ENGINE': 'xmodule.modulestore.mongo.DraftMongoModuleStore', 'DOC_STORE_CONFIG': {'db': 'openedx', 'host': 'mongodb', 'replicaSet': None, 'password': None, 'port': 27017, 'user': None, 'collection': 'modulestore', 'ssl': False, 'socketTimeoutMS': 6000, 'connectTimeoutMS': 2000, 'auth_source': None, 'read_preference': 'SECONDARY_PREFERRED', 'connect': False, 'authsource': 'admin'}, 'OPTIONS': {'default_class': 'xmodule.hidden_block.HiddenBlock', 'fs_root': '/openedx/data/modulestore', 'render_template': 'common.djangoapps.edxmako.shortcuts.render_to_string'}}]}}}
OAUTH_ENFORCE_SECURE = False
OPENEDX_LEARNING = {'MEDIA': {'BACKEND': 'django.core.files.storage.FileSystemStorage', 'OPTIONS': {'location': '/openedx/media-private/openedx-learning'}}}
ORA2_FILEUPLOAD_BACKEND = 'filesystem'
ORA2_FILEUPLOAD_CACHE_NAME = 'ora2-storage'
ORA2_FILEUPLOAD_ROOT = '/openedx/data/ora2'
PAYMENT_SUPPORT_EMAIL = 'contact@local.overhang.io'
PRESS_EMAIL = 'contact@local.overhang.io'
PROFILE_IMAGE_BACKEND['options']['location'] = '/openedx/media/profile-images/'
REGISTRATION_EXTRA_FIELDS['honor_code'] = 'hidden'
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False
SERVER_EMAIL = 'contact@local.overhang.io'
SESSION_COOKIE_SAMESITE = 'Lax'
SETTINGS_MODULE = 'lms.envs.tutor.production'
SILENCED_SYSTEM_CHECKS = ['2_0.W001', 'fields.W903']
SITE_ID = 2
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}
TECH_SUPPORT_EMAIL = 'contact@local.overhang.io'
UNIVERSITY_EMAIL = 'contact@local.overhang.io'
VIDEO_IMAGE_SETTINGS['STORAGE_KWARGS'] = {'location': '/openedx/media/'}
VIDEO_TRANSCRIPTS_SETTINGS['STORAGE_KWARGS'] = {'location': '/openedx/media/'}
X_FRAME_OPTIONS = 'SAMEORIGIN'
