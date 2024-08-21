# @@@@@@@@@ lms/envs/common.py
"""
This is the common settings file, intended to set sane defaults.

If you wish to override some of the settings set here without needing to specify
everything, you should create a new settings file that imports the content of this
one and then overrides anything you wish to make overridable.

Some known files that extend this one:

- `production.py` - This file loads overrides from a yaml settings file and uses that
    to override the settings set in this file.


Conventions
-----------

1. Extending a List Setting

    Sometimes settings take the form of a list and rather than replacing the
    whole list, we want to add items to the list. eg. CELERY_IMPORTS.

    In this case, it is recommended that a new variable created in your extended
    file that contains the word `EXTRA` and enough of the base variable to easily
    let people map between the two items.

    Examples:
        - CELERY_EXTRA_IMPORTS  (preferred format)
        - EXTRA_MIDDLEWARE_CLASSES
        - XBLOCK_EXTRA_MIXINS  (preferred format)

    The preferred format for the name of the new setting (e.g. `CELERY_EXTRA_IMPORTS`) is to use
    the same prefix (e.g. `CELERY`) of the setting that is being appended (e.g. `CELERY_IMPORTS`).
"""

# We intentionally define lots of variables that aren't used
# pylint: disable=unused-import

# Pylint gets confused by path.py instances, which report themselves as class
# objects. As a result, pylint applies the wrong regex in validating names,
# and throws spurious errors. Therefore, we disable invalid-name checking.
# pylint: disable=invalid-name

import importlib.util
import sys
import os

import django
from corsheaders.defaults import default_headers as corsheaders_default_headers
from path import Path as path
from django.utils.translation import gettext_lazy as _
from enterprise.constants import (
    ENTERPRISE_ADMIN_ROLE,
    ENTERPRISE_CATALOG_ADMIN_ROLE,
    ENTERPRISE_DASHBOARD_ADMIN_ROLE,
    ENTERPRISE_ENROLLMENT_API_ADMIN_ROLE,
    ENTERPRISE_FULFILLMENT_OPERATOR_ROLE,
    ENTERPRISE_REPORTING_CONFIG_ADMIN_ROLE,
    ENTERPRISE_SSO_ORCHESTRATOR_OPERATOR_ROLE,
    ENTERPRISE_OPERATOR_ROLE,
    SYSTEM_ENTERPRISE_PROVISIONING_ADMIN_ROLE,
    PROVISIONING_ENTERPRISE_CUSTOMER_ADMIN_ROLE,
    PROVISIONING_PENDING_ENTERPRISE_CUSTOMER_ADMIN_ROLE,
)

from openedx.core.constants import COURSE_KEY_REGEX, COURSE_KEY_PATTERN, COURSE_ID_PATTERN
from openedx.core.djangoapps.theming.helpers_dirs import (
    get_themes_unchecked,
    get_theme_base_dirs_from_settings
)
from openedx.core.lib.derived import derived, derived_collection_entry
from openedx.core.release import doc_version
from lms.djangoapps.lms_xblock.mixin import LmsBlockMixin

################################### FEATURES ###################################
# .. setting_name: PLATFORM_NAME
# .. setting_default: Your Platform Name Here
# .. setting_description: The display name of the platform to be used in
#     templates/emails/etc.
PLATFORM_NAME = _('Your Platform Name Here')
PLATFORM_DESCRIPTION = _('Your Platform Description Here')
CC_MERCHANT_NAME = PLATFORM_NAME

PLATFORM_FACEBOOK_ACCOUNT = "http://www.facebook.com/YourPlatformFacebookAccount"
PLATFORM_TWITTER_ACCOUNT = "@YourPlatformTwitterAccount"

ENABLE_JASMINE = False

LMS_ROOT_URL = 'https://localhost:18000'
LMS_INTERNAL_ROOT_URL = LMS_ROOT_URL
LMS_ENROLLMENT_API_PATH = "/api/enrollment/v1/"

# List of logout URIs for each IDA that the learner should be logged out of when they logout of the LMS. Only applies to
# IDA for which the social auth flow uses DOT (Django OAuth Toolkit).
IDA_LOGOUT_URI_LIST = []

# Features
FEATURES = {
    # .. toggle_name: FEATURES['DISPLAY_DEBUG_INFO_TO_STAFF']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Add a "Staff Debug" button to course blocks for debugging
    #   by course staff.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-09-04
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/2425
    'DISPLAY_DEBUG_INFO_TO_STAFF': True,

    # .. toggle_name: FEATURES['DISPLAY_HISTOGRAMS_TO_STAFF']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: This displays histograms in the Staff Debug Info panel to course staff.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-02-13
    # .. toggle_warning: Generating histograms requires scanning the courseware_studentmodule table on each view. This
    #   can make staff access to courseware very slow on large courses.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/2425
    'DISPLAY_HISTOGRAMS_TO_STAFF': False,  # For large courses this slows down courseware access for staff.

    'REROUTE_ACTIVATION_EMAIL': False,  # nonempty string = address for all activation emails

    # .. toggle_name: FEATURES['DISABLE_START_DATES']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When True, all courses will be active, regardless of start
    #   date.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2012-07-24
    # .. toggle_warning: This will cause ALL courses to be immediately visible.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/17913
    ## DO NOT SET TO True IN THIS FILE
    ## Doing so will cause all courses to be released on production
    'DISABLE_START_DATES': False,

    # .. toggle_name: FEATURES['ENABLE_DISCUSSION_SERVICE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: When True, it will enable the Discussion tab in courseware for all courses. Setting this
    #   to False will not contain inline discussion components and discussion tab in any courses.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2012-08-14
    # .. toggle_warning: If the discussion panel is present in the course and the value for this flag is False then,
    #   attempting to expand those components will cause errors. So, this should only be set to False with an LMS that
    #   is running courses that do not contain discussion components.
    #   For consistency in user-experience, keep the value in sync with the setting of the same name in the CMS.
    'ENABLE_DISCUSSION_SERVICE': True,

    # .. toggle_name: FEATURES['ENABLE_TEXTBOOK']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Add PDF and HTML textbook tabs to the courseware.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-03-27
    # .. toggle_warning: For consistency in user-experience, keep the value in sync with the setting of the same name
    #   in the CMS.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/3064
    'ENABLE_TEXTBOOK': True,

    # .. toggle_name: FEATURES['ENABLE_DISCUSSION_HOME_PANEL']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Hides or displays a welcome panel under the Discussion tab, which includes a subscription
    #   on/off setting for discussion digest emails.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-07-30
    # .. toggle_warning: This should remain off in production until digest notifications are online.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/520
    'ENABLE_DISCUSSION_HOME_PANEL': False,

    # .. toggle_name: FEATURES['ENABLE_DISCUSSION_EMAIL_DIGEST']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set this to True if you want the discussion digest emails
    #   enabled automatically for new users. This will be set on all new account
    #   registrations.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-08-19
    # .. toggle_target_removal_date: None
    # .. toggle_warning: It is not recommended to enable this feature if ENABLE_DISCUSSION_HOME_PANEL is not enabled,
    #   since subscribers who receive digests in that case will only be able to unsubscribe via links embedded in
    #   their emails, and they will have no way to resubscribe.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/4891
    'ENABLE_DISCUSSION_EMAIL_DIGEST': False,

    # .. toggle_name: FEATURES['ENABLE_UNICODE_USERNAME']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set this to True to allow unicode characters in username. Enabling this will also
    #   automatically enable SOCIAL_AUTH_CLEAN_USERNAMES. When this is enabled, usernames will have to match the
    #   regular expression defined by USERNAME_REGEX_PARTIAL.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-06-27
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/14729
    'ENABLE_UNICODE_USERNAME': False,

    # .. toggle_name: FEATURES['ENABLE_DJANGO_ADMIN_SITE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Set to False if you want to disable Django's admin site.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-09-26
    # .. toggle_warning: It is not recommended to disable this feature as there are many settings available on
    #  Django's admin site and will be inaccessible to the superuser.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/829
    'ENABLE_DJANGO_ADMIN_SITE': True,
    'ENABLE_LMS_MIGRATION': False,

    # .. toggle_name: FEATURES['ENABLE_MASQUERADE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: None
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-04-13
    'ENABLE_MASQUERADE': True,

    # .. toggle_name: FEATURES['DISABLE_LOGIN_BUTTON']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Removes the display of the login button in the navigation bar.
    #   Change is only at the UI level. Used in systems where login is automatic, eg MIT SSL
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-12-03
    'DISABLE_LOGIN_BUTTON': False,

    # .. toggle_name: FEATURES['ENABLE_OAUTH2_PROVIDER']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enable this feature to allow this Open edX platform to be an OAuth2 authentication
    #   provider. This is necessary to enable some other features, such as the REST API for the mobile application.
    # .. toggle_use_cases: temporary
    # .. toggle_creation_date: 2014-09-09
    # .. toggle_target_removal_date: None
    # .. toggle_warning: This temporary feature toggle does not have a target removal date.
    'ENABLE_OAUTH2_PROVIDER': False,

    # .. toggle_name: FEATURES['ENABLE_XBLOCK_VIEW_ENDPOINT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enable an API endpoint, named "xblock_view", to serve rendered XBlock views. This might be
    #   used by external applications. See for instance jquery-xblock (now unmaintained):
    #   https://github.com/openedx/jquery-xblock
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-03-14
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/2968
    'ENABLE_XBLOCK_VIEW_ENDPOINT': False,

    # Allows to configure the LMS to provide CORS headers to serve requests from other
    # domains
    'ENABLE_CORS_HEADERS': False,

    # Can be turned off if course lists need to be hidden. Effects views and templates.
    # .. toggle_name: FEATURES['COURSES_ARE_BROWSABLE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: When this is set to True, all the courses will be listed on the /courses page and Explore
    #   Courses link will be visible. Set to False if courses list and Explore Courses link need to be hidden.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-09-28
    # .. toggle_warning: This Effects views and templates.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/1073
    'COURSES_ARE_BROWSABLE': True,

    # Can be turned off to disable the help link in the navbar
    # .. toggle_name: FEATURES['ENABLE_HELP_LINK']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: When True, a help link is displayed on the main navbar. Set False to hide it.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2021-03-05
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/26106
    'ENABLE_HELP_LINK': True,

    # .. toggle_name: FEATURES['HIDE_DASHBOARD_COURSES_UNTIL_ACTIVATED']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When set, it hides the Courses list on the Learner Dashboard page if the learner has not
    #   yet activated the account and not enrolled in any courses.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2018-05-18
    # .. toggle_tickets: https://openedx.atlassian.net/browse/OSPR-1814
    'HIDE_DASHBOARD_COURSES_UNTIL_ACTIVATED': False,

    # .. toggle_name: FEATURES['ENABLE_STUDENT_HISTORY_VIEW']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: This provides a UI to show a student's submission history in a problem by the Staff Debug
    #   tool. Set to False if you want to hide Submission History from the courseware page.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-02-15
    # .. toggle_tickets: https://github.com/openedx/edx-platform/commit/8f17e6ae9ed76fa75b3caf867b65ccb632cb6870
    'ENABLE_STUDENT_HISTORY_VIEW': True,

    # Turn on a page that lets staff enter Python code to be run in the
    # sandbox, for testing whether it's enabled properly.
    'ENABLE_DEBUG_RUN_PYTHON': False,

    # Enable URL that shows information about the status of various services
    'ENABLE_SERVICE_STATUS': False,

    # Don't autoplay videos for students
    'AUTOPLAY_VIDEOS': False,

    # Move the student to next page when a video finishes. Set to True to show
    # an auto-advance button in videos. If False, videos never auto-advance.
    'ENABLE_AUTOADVANCE_VIDEOS': False,

    # Enable instructor dash to submit background tasks
    'ENABLE_INSTRUCTOR_BACKGROUND_TASKS': True,

    # Enable instructor to assign individual due dates
    # Note: In order for this feature to work, you must also add
    # 'lms.djangoapps.courseware.student_field_overrides.IndividualStudentOverrideProvider' to
    # the setting FIELD_OVERRIDE_PROVIDERS, in addition to setting this flag to
    # True.
    'INDIVIDUAL_DUE_DATES': False,

    # .. toggle_name: CUSTOM_COURSES_EDX
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to enable Custom Courses for edX, a feature that is more commonly known as
    #   CCX. Documentation for configuring and using this feature is available at
    #   https://edx.readthedocs.io/projects/open-edx-ca/en/latest/set_up_course/custom_courses.html
    # .. toggle_warning: When set to true, 'lms.djangoapps.ccx.overrides.CustomCoursesForEdxOverrideProvider' will
    #    be added to MODULESTORE_FIELD_OVERRIDE_PROVIDERS
    # .. toggle_use_cases: opt_in, circuit_breaker
    # .. toggle_creation_date: 2015-04-10
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/6636
    'CUSTOM_COURSES_EDX': False,

    # Toggle to enable certificates of courses on dashboard
    'ENABLE_VERIFIED_CERTIFICATES': False,
    # Settings for course import olx validation
    'ENABLE_COURSE_OLX_VALIDATION': False,

    # .. toggle_name: FEATURES['DISABLE_HONOR_CERTIFICATES']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to disable honor certificates. Typically used when your installation only
    #   allows verified certificates, like courses.edx.org.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2019-05-14
    # .. toggle_tickets: https://openedx.atlassian.net/browse/PROD-269
    'DISABLE_HONOR_CERTIFICATES': False,  # Toggle to disable honor certificates

    'DISABLE_AUDIT_CERTIFICATES': False,  # Toggle to disable audit certificates

    # .. toggle_name: FEATURES['AUTOMATIC_AUTH_FOR_TESTING']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to perform acceptance and load test. Auto auth view is responsible for load
    #    testing and is controlled by this feature flag. Session verification (of CacheBackedAuthenticationMiddleware)
    #    is a security feature, but it can be turned off by enabling this feature flag.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-07-25
    # .. toggle_warning: If this has been set to True then the account activation email will be skipped.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/417
    'AUTOMATIC_AUTH_FOR_TESTING': False,

    # .. toggle_name: FEATURES['RESTRICT_AUTOMATIC_AUTH']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Prevent auto auth from creating superusers or modifying existing users. Auto auth is a
    #   mechanism where superusers can simply modify attributes of other users by accessing the "/auto_auth url" with
    #   the right
    #   querystring parameters.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2018-05-07
    # .. toggle_tickets: https://openedx.atlassian.net/browse/TE-2545
    'RESTRICT_AUTOMATIC_AUTH': True,

    # .. toggle_name: FEATURES['ENABLE_LOGIN_MICROFRONTEND']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enable the login micro frontend.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2018-05-07
    # .. toggle_warning: The login MFE domain name should be listed in LOGIN_REDIRECT_WHITELIST.
    'ENABLE_LOGIN_MICROFRONTEND': False,

    # .. toggle_name: FEATURES['SKIP_EMAIL_VALIDATION']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Turn this on to skip sending emails for user validation.
    #   Beware, as this leaves the door open to potential spam abuse.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2018-05-07
    # .. toggle_warning: The login MFE domain name should be listed in LOGIN_REDIRECT_WHITELIST.
    'SKIP_EMAIL_VALIDATION': False,

    # .. toggle_name: FEATURES['ENABLE_COSMETIC_DISPLAY_PRICE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enable the display of "cosmetic_display_price", set in a course advanced settings. This
    #   cosmetic price is used when there is no registration price associated to the course.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-10-10
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/6876
    # .. toggle_warning: The use case of this feature toggle is uncertain.
    'ENABLE_COSMETIC_DISPLAY_PRICE': False,

    # Automatically approve student identity verification attempts
    # .. toggle_name: FEATURES['AUTOMATIC_VERIFY_STUDENT_IDENTITY_FOR_TESTING']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: If set to True, then we want to skip posting anything to Software Secure. Bypass posting
    #   anything to Software Secure if the auto verify feature for testing is enabled. We actually don't even create
    #   the message because that would require encryption and message signing that rely on settings.VERIFY_STUDENT
    #   values that aren't set in dev. So we just pretend like we successfully posted and automatically approve student
    #   identity verification attempts.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2013-10-03
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/1184
    'AUTOMATIC_VERIFY_STUDENT_IDENTITY_FOR_TESTING': False,

    # Maximum number of rows to include in the csv file for downloading problem responses.
    'MAX_PROBLEM_RESPONSES_COUNT': 5000,

    'ENABLED_PAYMENT_REPORTS': [
        "refund_report",
        "itemized_purchase_report",
        "university_revenue_share",
        "certificate_status"
    ],

    # Turn off account locking if failed login attempts exceeds a limit
    # .. toggle_name: FEATURES['ENABLE_MAX_FAILED_LOGIN_ATTEMPTS']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: This feature will keep track of the number of failed login attempts on a given user's
    #   email. If the number of consecutive failed login attempts - without a successful login at some point - reaches
    #   a configurable threshold (default 6), then the account will be locked for a configurable amount of seconds
    #   (30 minutes) which will prevent additional login attempts until this time period has passed. If a user
    #   successfully logs in, all the counter which tracks the number of failed attempts will be reset back to 0. If
    #   set to False then account locking will be disabled for failed login attempts.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-01-30
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/2331
    'ENABLE_MAX_FAILED_LOGIN_ATTEMPTS': True,

    # Hide any Personally Identifiable Information from application logs
    'SQUELCH_PII_IN_LOGS': True,

    # .. toggle_name: FEATURES['EMBARGO']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Turns on embargo functionality, which blocks users from
    #   the site or courses based on their location. Embargo can restrict users by states
    #   and whitelist/blacklist (IP Addresses (ie. 10.0.0.0), Networks (ie. 10.0.0.0/24)), or the user profile country.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-02-27
    # .. toggle_target_removal_date: None
    # .. toggle_warning: reverse proxy should be configured appropriately for example Client IP address headers
    #   (e.g HTTP_X_FORWARDED_FOR) should be configured.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/2749
    'EMBARGO': False,

    # Whether the Wiki subsystem should be accessible via the direct /wiki/ paths. Setting this to True means
    # that people can submit content and modify the Wiki in any arbitrary manner. We're leaving this as True in the
    # defaults, so that we maintain current behavior
    'ALLOW_WIKI_ROOT_ACCESS': True,

    # .. toggle_name: FEATURES['ENABLE_THIRD_PARTY_AUTH']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Turn on third-party auth. Disabled for now because full implementations are not yet
    #   available. Remember to run migrations if you enable this; we don't create tables by default. This feature can
    #   be enabled on a per-site basis. When enabling this feature, remember to define the allowed authentication
    #   backends with the AUTHENTICATION_BACKENDS setting.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-09-15
    'ENABLE_THIRD_PARTY_AUTH': False,

    # .. toggle_name: FEATURES['ENABLE_MKTG_SITE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Toggle to enable alternate urls for marketing links.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-03-24
    # .. toggle_warning: When this is enabled, the MKTG_URLS setting should be defined. The use case of this feature
    #   toggle is uncertain.
    'ENABLE_MKTG_SITE': False,

    # Prevent concurrent logins per user
    'PREVENT_CONCURRENT_LOGINS': True,

    # .. toggle_name: FEATURES['ALWAYS_REDIRECT_HOMEPAGE_TO_DASHBOARD_FOR_AUTHENTICATED_USER']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: When a logged in user goes to the homepage ('/') the user will be redirected to the
    #   dashboard page when this flag is set to True - this is default Open edX behavior. Set to False to not redirect
    #   the user.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2014-09-16
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/5220
    'ALWAYS_REDIRECT_HOMEPAGE_TO_DASHBOARD_FOR_AUTHENTICATED_USER': True,

    # .. toggle_name: FEATURES['ENABLE_COURSE_SORTING_BY_START_DATE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: When a user goes to the homepage ('/') the user sees the courses listed in the
    #   announcement dates order - this is default Open edX behavior. Set to True to change the course sorting behavior
    #   by their start dates, latest first.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-03-27
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/7548
    'ENABLE_COURSE_SORTING_BY_START_DATE': True,

    # .. toggle_name: FEATURES['ENABLE_COURSE_HOME_REDIRECT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: When enabled, along with the ENABLE_MKTG_SITE feature toggle, users who attempt to access a
    #   course "about" page will be redirected to the course home url.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2019-01-15
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/19604
    'ENABLE_COURSE_HOME_REDIRECT': True,

    # Expose Mobile REST API. Note that if you use this, you must also set
    # ENABLE_OAUTH2_PROVIDER to True
    'ENABLE_MOBILE_REST_API': False,

    # .. toggle_name: FEATURES['ENABLE_COMBINED_LOGIN_REGISTRATION_FOOTER']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Display the standard footer in the login page. This feature can be overridden by a site-
    #   specific configuration.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2016-06-24
    # .. toggle_tickets: https://openedx.atlassian.net/browse/OSPR-1320
    'ENABLE_COMBINED_LOGIN_REGISTRATION_FOOTER': False,

    # Enable organizational email opt-in
    'ENABLE_MKTG_EMAIL_OPT_IN': False,

    # .. toggle_name: FEATURES['ENABLE_FOOTER_MOBILE_APP_LINKS']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True if you want show the mobile app links (Apple App Store & Google Play Store) in
    #   the footer.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-01-13
    # .. toggle_warning: If you set this to True then you should also set your mobile application's app store and play
    #   store URLs in the MOBILE_STORE_URLS settings dictionary. These links are not part of the default theme. If you
    #   want these links on your footer then you should use the edx.org theme.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/6588
    'ENABLE_FOOTER_MOBILE_APP_LINKS': False,

    # Let students save and manage their annotations
    # .. toggle_name: FEATURES['ENABLE_EDXNOTES']
    # .. toggle_implementation: SettingToggle
    # .. toggle_default: False
    # .. toggle_description: This toggle enables the students to save and manage their annotations in the
    #   course using the notes service. The bulk of the actual work in storing the notes is done by
    #   a separate service (see the edx-notes-api repo).
    # .. toggle_warning: Requires the edx-notes-api service properly running and to have configured the django settings
    #   EDXNOTES_INTERNAL_API and EDXNOTES_PUBLIC_API. If you update this setting, also update it in Studio.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-01-04
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/6321
    'ENABLE_EDXNOTES': False,

    # Toggle to enable coordination with the Publisher tool (keep in sync with cms/envs/common.py)
    'ENABLE_PUBLISHER': False,

    # Milestones application flag
    'MILESTONES_APP': False,

    # Prerequisite courses feature flag
    'ENABLE_PREREQUISITE_COURSES': False,

    # For easily adding modes to courses during acceptance testing
    'MODE_CREATION_FOR_TESTING': False,

    # For caching programs in contexts where the LMS can only
    # be reached over HTTP.
    'EXPOSE_CACHE_PROGRAMS_ENDPOINT': False,

    # Courseware search feature
    # .. toggle_name: FEATURES['ENABLE_COURSEWARE_SEARCH']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When enabled, this adds a Search the course widget on the course outline and courseware
    #   pages for searching courseware data.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-01-29
    # .. toggle_warning: In order to get this working, your courses data should be indexed in Elasticsearch. You will
    #   see the search widget on the courseware page only if the DISABLE_COURSE_OUTLINE_PAGE_FLAG is set.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/6506
    'ENABLE_COURSEWARE_SEARCH': False,

    # .. toggle_name: FEATURES['ENABLE_COURSEWARE_SEARCH_FOR_COURSE_STAFF']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When enabled, this adds a Search the course widget on the course outline and courseware
    #   pages for searching courseware data but for course staff users only.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2019-12-06
    # .. toggle_warning: In order to get this working, your courses data should be indexed in Elasticsearch. If
    #   ENABLE_COURSEWARE_SEARCH is enabled then the search widget will be visible to all learners and this flag's
    #   value does not matter in that case. This flag is enabled in devstack by default.
    # .. toggle_tickets: https://openedx.atlassian.net/browse/TNL-6931
    'ENABLE_COURSEWARE_SEARCH_FOR_COURSE_STAFF': False,

    # Dashboard search feature
    # .. toggle_name: FEATURES['ENABLE_DASHBOARD_SEARCH']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When enabled, this adds a Search Your Courses widget on the dashboard page for searching
    #   courseware data.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-01-29
    # .. toggle_warning: In order to get this working, your courses data should be indexed in Elasticsearch.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/6506
    'ENABLE_DASHBOARD_SEARCH': False,

    # log all information from cybersource callbacks
    'LOG_POSTPAY_CALLBACKS': True,

    # .. toggle_name: FEATURES['LICENSING']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Toggle platform-wide course licensing. The course.license attribute is then used to append
    #   license information to the courseware.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-05-14
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/7315
    'LICENSING': False,

    # .. toggle_name: FEATURES['CERTIFICATES_HTML_VIEW']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to enable course certificates on your instance of Open edX.
    # .. toggle_warning: You must enable this feature flag in both Studio and the LMS and complete the configuration tasks
    #   described here:
    #   https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/enable_certificates.html  pylint: disable=line-too-long,useless-suppression
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-03-13
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/7113
    'CERTIFICATES_HTML_VIEW': False,

    # .. toggle_name: FEATURES['CUSTOM_CERTIFICATE_TEMPLATES_ENABLED']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to enable custom certificate templates which are configured via Django admin.
    # .. toggle_warning: None
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-08-13
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: https://openedx.atlassian.net/browse/SOL-1044
    'CUSTOM_CERTIFICATE_TEMPLATES_ENABLED': False,

    # .. toggle_name: FEATURES['ENABLE_COURSE_DISCOVERY']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Add a course search widget to the LMS for searching courses. When this is enabled, the
    #   latest courses are no longer displayed on the LMS landing page. Also, an "Explore Courses" item is added to the
    #   navbar.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-04-23
    # .. toggle_target_removal_date: None
    # .. toggle_warning: The COURSE_DISCOVERY_MEANINGS setting should be properly defined.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/7845
    'ENABLE_COURSE_DISCOVERY': False,

    # .. toggle_name: FEATURES['ENABLE_COURSE_FILENAME_CCX_SUFFIX']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: If set to True, CCX ID will be included in the generated filename for CCX courses.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2021-03-16
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: None
    # .. toggle_warning: Turning this feature ON will affect all generated filenames which are related to CCX courses.
    'ENABLE_COURSE_FILENAME_CCX_SUFFIX': False,

    # Setting for overriding default filtering facets for Course discovery
    # COURSE_DISCOVERY_FILTERS = ["org", "language", "modes"]

    # Software secure fake page feature flag
    'ENABLE_SOFTWARE_SECURE_FAKE': False,

    # Teams feature
    'ENABLE_TEAMS': True,

    # Show video bumper in LMS
    'ENABLE_VIDEO_BUMPER': False,

    # How many seconds to show the bumper again, default is 7 days:
    'SHOW_BUMPER_PERIODICITY': 7 * 24 * 3600,

    # .. toggle_name: FEATURES['ENABLE_SPECIAL_EXAMS']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enable to use special exams, aka timed and proctored exams.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-09-04
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/9744
    'ENABLE_SPECIAL_EXAMS': False,

    # .. toggle_name: FEATURES['ENABLE_LTI_PROVIDER']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When set to True, Open edX site can be used as an LTI Provider to other systems
    #    and applications.
    # .. toggle_warning: After enabling this feature flag there are multiple steps involved to configure edX
    #    as LTI provider. Full guide is available here:
    #    https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/lti/index.html
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2015-04-24
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/7689
    'ENABLE_LTI_PROVIDER': False,

    # .. toggle_name: FEATURES['SHOW_HEADER_LANGUAGE_SELECTOR']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When set to True, language selector will be visible in the header.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-05-25
    # .. toggle_warning: You should set the languages in the DarkLangConfig table to get this working. If you have
    #   not set any languages in the DarkLangConfig table then the language selector will not be visible in the header.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/15133
    'SHOW_HEADER_LANGUAGE_SELECTOR': False,

    # At edX it's safe to assume that English transcripts are always available
    # This is not the case for all installations.
    # The default value in {lms,cms}/envs/common.py and xmodule/tests/test_video.py should be consistent.
    'FALLBACK_TO_ENGLISH_TRANSCRIPTS': True,

    # .. toggle_name: FEATURES['SHOW_FOOTER_LANGUAGE_SELECTOR']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When set to True, language selector will be visible in the footer.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-05-25
    # .. toggle_warning: LANGUAGE_COOKIE_NAME is required to use footer-language-selector, set it if it has not been set.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/15133
    'SHOW_FOOTER_LANGUAGE_SELECTOR': False,

    # .. toggle_name: FEATURES['ENABLE_CSMH_EXTENDED']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Write Courseware Student Module History (CSMH) to the extended table: this logs all
    #   student activities to MySQL, in a separate database.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2020-11-05
    # .. toggle_warning: Even though most Open edX instances run with a separate CSMH database, it may not always be
    #   the case. When disabling this feature flag, remember to remove "lms.djangoapps.coursewarehistoryextended"
    #   from the INSTALLED_APPS and the "StudentModuleHistoryExtendedRouter" from the DATABASE_ROUTERS.
    'ENABLE_CSMH_EXTENDED': True,

    # Read from both the CSMH and CSMHE history tables.
    # This is the default, but can be disabled if all history
    # lives in the Extended table, saving the frontend from
    # making multiple queries.
    'ENABLE_READING_FROM_MULTIPLE_HISTORY_TABLES': True,

    # Set this to False to facilitate cleaning up invalid xml from your modulestore.
    'ENABLE_XBLOCK_XML_VALIDATION': True,

    # .. toggle_name: FEATURES['ALLOW_PUBLIC_ACCOUNT_CREATION']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Allow public account creation. If this is disabled, users will no longer have access to
    #   the signup page.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-04-12
    # .. toggle_tickets: https://openedx.atlassian.net/browse/YONK-513
    'ALLOW_PUBLIC_ACCOUNT_CREATION': True,

    # .. toggle_name: FEATURES['SHOW_REGISTRATION_LINKS']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Allow registration links. If this is disabled, users will no longer see buttons to the
    #   the signup page.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2023-03-27
    'SHOW_REGISTRATION_LINKS': True,

    # .. toggle_name: FEATURES['ENABLE_COOKIE_CONSENT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enable header banner for cookie consent using this service:
    #   https://cookieconsent.insites.com/
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-03-03
    # .. toggle_tickets: https://openedx.atlassian.net/browse/OSPR-1560
    'ENABLE_COOKIE_CONSENT': False,

    # Whether or not the dynamic EnrollmentTrackUserPartition should be registered.
    'ENABLE_ENROLLMENT_TRACK_USER_PARTITION': True,

    # Enable one click program purchase
    # See LEARNER-493
    'ENABLE_ONE_CLICK_PROGRAM_PURCHASE': False,

    # .. toggle_name: FEATURES['ALLOW_EMAIL_ADDRESS_CHANGE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Allow users to change their email address on the Account Settings page. If this is
    #   disabled, users will not be able to change their email address.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-06-26
    # .. toggle_tickets: https://openedx.atlassian.net/browse/OSPR-1735
    'ALLOW_EMAIL_ADDRESS_CHANGE': True,

    # .. toggle_name: FEATURES['ENABLE_BULK_ENROLLMENT_VIEW']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When set to True the bulk enrollment view is enabled and one can use it to enroll multiple
    #   users in a course using bulk enrollment API endpoint (/api/bulk_enroll/v1/bulk_enroll).
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-07-15
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/15006
    'ENABLE_BULK_ENROLLMENT_VIEW': False,

    # Set to enable Enterprise integration
    'ENABLE_ENTERPRISE_INTEGRATION': False,

    # .. toggle_name: FEATURES['ENABLE_HTML_XBLOCK_STUDENT_VIEW_DATA']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Whether HTML Block returns HTML content with the Course Blocks API when the API
    #   is called with student_view_data=html query parameter.
    # .. toggle_warning: Because the Course Blocks API caches its data, the cache must be cleared (e.g. by
    #   re-publishing the course) for changes to this flag to take effect.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-08-28
    # .. toggle_tickets: https://openedx.atlassian.net/browse/OSPR-1880
    'ENABLE_HTML_XBLOCK_STUDENT_VIEW_DATA': False,

    # .. toggle_name: FEATURES['ENABLE_PASSWORD_RESET_FAILURE_EMAIL']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Whether to send an email for failed password reset attempts or not. This happens when a
    #   user asks for a password reset but they don't have an account associated to their email. This is useful for
    #   notifying users that they don't have an account associated with email addresses they believe they've registered
    #   with. This setting can be overridden by a site-specific configuration.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2017-07-20
    # .. toggle_tickets: https://openedx.atlassian.net/browse/OSPR-1832
    'ENABLE_PASSWORD_RESET_FAILURE_EMAIL': False,

    # Sets the default browser support. For more information go to http://browser-update.org/customize.html
    'UNSUPPORTED_BROWSER_ALERT_VERSIONS': "{i:10,f:-3,o:-3,s:-3,c:-3}",

    # .. toggle_name: FEATURES['ENABLE_ACCOUNT_DELETION']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: True
    # .. toggle_description: Whether to display the account deletion section on Account Settings page. Set to False to
    #   hide this section.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2018-06-01
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/18298
    'ENABLE_ACCOUNT_DELETION': True,

    # Enable feature to remove enrollments and users. Used to reset state of master's integration environments
    'ENABLE_ENROLLMENT_RESET': False,
    'DISABLE_MOBILE_COURSE_AVAILABLE': False,

    # .. toggle_name: FEATURES['ENABLE_CHANGE_USER_PASSWORD_ADMIN']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to enable changing a user password through django admin. This is disabled by
    #   default because enabling allows a method to bypass password policy.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2020-02-21
    # .. toggle_tickets: 'https://github.com/openedx/edx-platform/pull/21616'
    'ENABLE_CHANGE_USER_PASSWORD_ADMIN': False,

    # .. toggle_name: FEATURES['ENABLE_AUTHN_MICROFRONTEND']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Supports staged rollout of a new micro-frontend-based implementation of the logistration.
    # .. toggle_use_cases: temporary, open_edx
    # .. toggle_creation_date: 2020-09-08
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: 'https://github.com/openedx/edx-platform/pull/24908'
    # .. toggle_warning: Also set settings.AUTHN_MICROFRONTEND_URL for rollout. This temporary feature
    #   toggle does not have a target removal date.
    'ENABLE_AUTHN_MICROFRONTEND': os.environ.get("EDXAPP_ENABLE_AUTHN_MFE", False),

    ### ORA Feature Flags ###
    # .. toggle_name: FEATURES['ENABLE_ORA_ALL_FILE_URLS']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: A "work-around" feature toggle meant to help in cases where some file uploads are not
    #   discoverable.  If enabled, will iterate through all possible file key suffixes up to the max for displaying
    #   file metadata in staff assessments.
    # .. toggle_use_cases: temporary
    # .. toggle_creation_date: 2020-03-03
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: https://openedx.atlassian.net/browse/EDUCATOR-4951
    # .. toggle_warning: This temporary feature toggle does not have a target removal date.
    'ENABLE_ORA_ALL_FILE_URLS': False,

    # .. toggle_name: FEATURES['ENABLE_ORA_USER_STATE_UPLOAD_DATA']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: A "work-around" feature toggle meant to help in cases where some file uploads are not
    #   discoverable.  If enabled, will pull file metadata from StudentModule.state for display in staff assessments.
    # .. toggle_use_cases: temporary
    # .. toggle_creation_date: 2020-03-03
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: https://openedx.atlassian.net/browse/EDUCATOR-4951
    # .. toggle_warning: This temporary feature toggle does not have a target removal date.
    'ENABLE_ORA_USER_STATE_UPLOAD_DATA': False,

    # .. toggle_name: FEATURES['ENABLE_ORA_USERNAMES_ON_DATA_EXPORT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to add deanonymized usernames to ORA data
    #   report.
    # .. toggle_use_cases: temporary
    # .. toggle_creation_date: 2020-06-11
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: https://openedx.atlassian.net/browse/TNL-7273
    # .. toggle_warning: This temporary feature toggle does not have a target removal date.
    'ENABLE_ORA_USERNAMES_ON_DATA_EXPORT': False,

    # .. toggle_name: FEATURES['ENABLE_COURSE_ASSESSMENT_GRADE_CHANGE_SIGNAL']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to start sending signals for assessment level grade updates. Notably, the only
    #   handler of this signal at the time of this writing sends assessment updates to enterprise integrated channels.
    # .. toggle_use_cases: temporary
    # .. toggle_creation_date: 2020-12-09
    # .. toggle_target_removal_date: 2021-02-01
    # .. toggle_tickets: https://openedx.atlassian.net/browse/ENT-3818
    'ENABLE_COURSE_ASSESSMENT_GRADE_CHANGE_SIGNAL': False,

    # .. toggle_name: FEATURES['ALLOW_ADMIN_ENTERPRISE_COURSE_ENROLLMENT_DELETION']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: If true, allows for the deletion of EnterpriseCourseEnrollment records via Django Admin.
    # .. toggle_use_cases: opt_in
    # .. toggle_creation_date: 2021-01-27
    # .. toggle_tickets: https://openedx.atlassian.net/browse/ENT-4022
    'ALLOW_ADMIN_ENTERPRISE_COURSE_ENROLLMENT_DELETION': False,

    # .. toggle_name: FEATURES['ENABLE_BULK_USER_RETIREMENT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to enable bulk user retirement through REST API. This is disabled by
    #   default.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2021-03-11
    # .. toggle_target_removal_date: None
    # .. toggle_warning: None
    # .. toggle_tickets: 'https://openedx.atlassian.net/browse/OSPR-5290'
    'ENABLE_BULK_USER_RETIREMENT': False,

    # .. toggle_name: FEATURES['ENABLE_V2_CERT_DISPLAY_SETTINGS']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Whether to use the reimagined certificates_display_behavior and certificate_available_date
    # .. settings. Will eventually become the default.
    # .. toggle_use_cases: temporary
    # .. toggle_creation_date: 2021-07-26
    # .. toggle_target_removal_date: 2021-10-01
    # .. toggle_tickets: 'https://openedx.atlassian.net/browse/MICROBA-1405'
    'ENABLE_V2_CERT_DISPLAY_SETTINGS': False,

    # .. toggle_name: FEATURES['ENABLE_INTEGRITY_SIGNATURE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Whether to display honor code agreement for learners before their first grade assignment
    # (https://github.com/edx/edx-name-affirmation)
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2022-02-15
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: 'https://openedx.atlassian.net/browse/MST-1348'
    'ENABLE_INTEGRITY_SIGNATURE': False,

    # .. toggle_name: FEATURES['ENABLE_LTI_PII_ACKNOWLEDGEMENT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enables the lti pii acknowledgement feature for a course
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2023-10
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: 'https://2u-internal.atlassian.net/browse/MST-2055'
    'ENABLE_LTI_PII_ACKNOWLEDGEMENT': False,

    # .. toggle_name: FEATURES['ENABLE_NEW_BULK_EMAIL_EXPERIENCE']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When true, replaces the bulk email tool found on the
    #   instructor dashboard with a link to the new communications MFE version instead.
    #   Setting the tool to false will leave the old bulk email tool experience in place.
    # .. toggle_use_cases: opt_in
    # .. toggle_creation_date: 2022-03-21
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: 'https://openedx.atlassian.net/browse/MICROBA-1758'
    'ENABLE_NEW_BULK_EMAIL_EXPERIENCE': False,

    # .. toggle_name: MARK_LIBRARY_CONTENT_BLOCK_COMPLETE_ON_VIEW
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: If enabled, the Library Content Block is marked as complete when users view it.
    #   Otherwise (by default), all children of this block must be completed.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2022-03-22
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/28268
    # .. toggle_warning: For consistency in user-experience, keep the value in sync with the setting of the same name
    #   in the LMS and CMS.
    'MARK_LIBRARY_CONTENT_BLOCK_COMPLETE_ON_VIEW': False,

    # .. toggle_name: FEATURES['DISABLE_UNENROLLMENT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to disable self-unenrollments via REST API.
    #   This also hides the "Unenroll" button on the Learner Dashboard.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2021-10-11
    # .. toggle_warning: For consistency in user experience, keep the value in sync with the setting of the same name
    #   in the LMS and CMS.
    # .. toggle_tickets: 'https://github.com/open-craft/edx-platform/pull/429'
    'DISABLE_UNENROLLMENT': False,

    # .. toggle_name: FEATURES['ENABLE_CERTIFICATES_IDV_REQUIREMENT']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Whether to enforce ID Verification requirements for course certificates generation
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2022-04-26
    # .. toggle_target_removal_date: None
    # .. toggle_tickets: 'https://openedx.atlassian.net/browse/MST-1458'
    'ENABLE_CERTIFICATES_IDV_REQUIREMENT': False,

    # .. toggle_name: FEATURES['DISABLE_ALLOWED_ENROLLMENT_IF_ENROLLMENT_CLOSED']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to disable enrollment for user invited to a course
    # .. if user is registering before enrollment start date or after enrollment end date
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2022-06-06
    # .. toggle_tickets: 'https://github.com/openedx/edx-platform/pull/29538'
    'DISABLE_ALLOWED_ENROLLMENT_IF_ENROLLMENT_CLOSED': False,

    # .. toggle_name: FEATURES['SEND_LEARNING_CERTIFICATE_LIFECYCLE_EVENTS_TO_BUS']
    # .. toggle_implementation: SettingToggle
    # .. toggle_default: False
    # .. toggle_description: When True, the system will publish certificate lifecycle signals to the event bus.
    #    This toggle is used to create the EVENT_BUS_PRODUCER_CONFIG setting.
    # .. toggle_warning: The default may be changed in a later release. See
    #    https://github.com/openedx/openedx-events/issues/265
    # .. toggle_use_cases: opt_in
    # .. toggle_creation_date: 2023-10-10
    # .. toggle_tickets: https://github.com/openedx/openedx-events/issues/210
    'SEND_LEARNING_CERTIFICATE_LIFECYCLE_EVENTS_TO_BUS': False,

    # .. toggle_name: FEATURES['ENABLE_GRADING_METHOD_IN_PROBLEMS']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enables the grading method feature in capa problems.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2024-03-22
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/33911
    'ENABLE_GRADING_METHOD_IN_PROBLEMS': False,

    # .. toggle_name: FEATURES['ENABLE_COURSEWARE_SEARCH_VERIFIED_REQUIRED']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: When enabled, the courseware search feature will only be enabled
    #   for users in a verified enrollment track.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2024-04-24
    'ENABLE_COURSEWARE_SEARCH_VERIFIED_ENROLLMENT_REQUIRED': False,

    # .. toggle_name: FEATURES['ENABLE_BLAKE2B_HASHING']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Enables the memcache to use the blake2b hash algorithm instead of depreciated md4 for keys
    #   exceeding 250 characters
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2024-04-02
    # .. toggle_target_removal_date: 2024-12-09
    # .. toggle_warning: For consistency, keep the value in sync with the setting of the same name in the LMS and CMS.
    # .. toggle_tickets: https://github.com/openedx/edx-platform/pull/34442
    'ENABLE_BLAKE2B_HASHING': False,

    # .. toggle_name: FEATURES['BADGES_ENABLED']
    # .. toggle_implementation: DjangoSetting
    # .. toggle_default: False
    # .. toggle_description: Set to True to enable badges functionality.
    # .. toggle_use_cases: open_edx
    # .. toggle_creation_date: 2024-04-02
    # .. toggle_target_removal_date: None
    'BADGES_ENABLED': False,
}

# Specifies extra XBlock fields that should available when requested via the Course Blocks API
# Should be a list of tuples of (block_type, field_name), where block_type can also be "*" for all block types.
# e.g. COURSE_BLOCKS_API_EXTRA_FIELDS = [  ('course', 'other_course_settings'), ("problem", "weight")  ]
COURSE_BLOCKS_API_EXTRA_FIELDS = []


ASSET_IGNORE_REGEX = r"(^\._.*$)|(^\.DS_Store$)|(^.*~$)"

# Used for A/B testing
DEFAULT_GROUPS = []

# If this is true, random scores will be generated for the purpose of debugging the profile graphs
GENERATE_PROFILE_SCORES = False

# .. setting_name: GRADEBOOK_FREEZE_DAYS
# .. setting_default: 30
# .. setting_description: Sets the number of days after which the gradebook will freeze following the course's end.
GRADEBOOK_FREEZE_DAYS = 30

# Used with XQueue
XQUEUE_WAITTIME_BETWEEN_REQUESTS = 5  # seconds
XQUEUE_INTERFACE = {
    'url': 'http://localhost:18040',
    'basic_auth': ['edx', 'edx'],
    'django_auth': {
        'username': 'lms',
        'password': 'password'
    }
}

# Used with Email sending
RETRY_ACTIVATION_EMAIL_MAX_ATTEMPTS = 5
RETRY_ACTIVATION_EMAIL_TIMEOUT = 0.5

# Software Secure request retry settings
# Time in seconds before a retry of the task should be 60 mints.
SOFTWARE_SECURE_REQUEST_RETRY_DELAY = 60 * 60
# Maximum of 6 retries before giving up.
SOFTWARE_SECURE_RETRY_MAX_ATTEMPTS = 6

RETRY_CALENDAR_SYNC_EMAIL_MAX_ATTEMPTS = 5

MARKETING_EMAILS_OPT_IN = False

# .. toggle_name: ENABLE_COPPA_COMPLIANCE
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When True, enforces COPPA compliance and removes YOB field from registration form and account
# .. settings page. Also hide YOB banner from profile page.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2021-10-27
# .. toggle_tickets: 'https://openedx.atlassian.net/browse/VAN-622'
ENABLE_COPPA_COMPLIANCE = False

############################# SET PATH INFORMATION #############################
PROJECT_ROOT = path(__file__).abspath().dirname().dirname()  # /edx-platform/lms
REPO_ROOT = PROJECT_ROOT.dirname()
COMMON_ROOT = REPO_ROOT / "common"
OPENEDX_ROOT = REPO_ROOT / "openedx"
XMODULE_ROOT = REPO_ROOT / "xmodule"
ENV_ROOT = REPO_ROOT.dirname()  # virtualenv dir /edx-platform is in
COURSES_ROOT = ENV_ROOT / "data"
NODE_MODULES_ROOT = REPO_ROOT / "node_modules"

DATA_DIR = COURSES_ROOT

# For geolocation ip database
GEOIP_PATH = REPO_ROOT / "common/static/data/geoip/GeoLite2-Country.mmdb"
# Where to look for a status message
STATUS_MESSAGE_PATH = ENV_ROOT / "status_message.json"

############################ Global Database Configuration #####################

DATABASE_ROUTERS = [
    'openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter',
    'edx_django_utils.db.read_replica.ReadReplicaRouter',
]

############################ Cache Configuration ###############################

CACHES = {
    'course_structure_cache': {
        'KEY_PREFIX': 'course_structure',
        'KEY_FUNCTION': 'common.djangoapps.util.memcache.safe_key',
        'LOCATION': ['localhost:11211'],
        'TIMEOUT': '604800',  # 1 week
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'use_pooling': True,
            'connect_timeout': 0.5
        }
    },
    'celery': {
        'KEY_PREFIX': 'celery',
        'KEY_FUNCTION': 'common.djangoapps.util.memcache.safe_key',
        'LOCATION': ['localhost:11211'],
        'TIMEOUT': '7200',
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'use_pooling': True,
            'connect_timeout': 0.5
        }
    },
    'mongo_metadata_inheritance': {
        'KEY_PREFIX': 'mongo_metadata_inheritance',
        'KEY_FUNCTION': 'common.djangoapps.util.memcache.safe_key',
        'LOCATION': ['localhost:11211'],
        'TIMEOUT': 300,
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'use_pooling': True,
            'connect_timeout': 0.5
        }
    },
    'staticfiles': {
        'KEY_FUNCTION': 'common.djangoapps.util.memcache.safe_key',
        'LOCATION': ['localhost:11211'],
        'KEY_PREFIX': 'staticfiles_general',
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'use_pooling': True,
            'connect_timeout': 0.5
        }
    },
    'default': {
        'VERSION': '1',
        'KEY_FUNCTION': 'common.djangoapps.util.memcache.safe_key',
        'LOCATION': ['localhost:11211'],
        'KEY_PREFIX': 'default',
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'use_pooling': True,
            'connect_timeout': 0.5
        }
    },
    'configuration': {
        'KEY_FUNCTION': 'common.djangoapps.util.memcache.safe_key',
        'LOCATION': ['localhost:11211'],
        'KEY_PREFIX': 'configuration',
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'use_pooling': True,
            'connect_timeout': 0.5
        }
    },
    'general': {
        'KEY_FUNCTION': 'common.djangoapps.util.memcache.safe_key',
        'LOCATION': ['localhost:11211'],
        'KEY_PREFIX': 'general',
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'use_pooling': True,
            'connect_timeout': 0.5
        }
    },
}

############################ OAUTH2 Provider ###################################
OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS = 365
OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS = 30

################################## DJANGO OAUTH TOOLKIT #######################################

# Scope description strings are presented to the user
# on the application authorization page. See
# lms/templates/oauth2_provider/authorize.html for details.
# Non-default scopes should be added directly to OAUTH2_PROVIDER['SCOPES'] below.
OAUTH2_DEFAULT_SCOPES = {
    'read': _('Read access'),
    'write': _('Write access'),
    'email': _('Know your email address'),
    'profile': _('Know your name and username'),
}

OAUTH2_PROVIDER = {
    'OAUTH2_VALIDATOR_CLASS': 'openedx.core.djangoapps.oauth_dispatch.dot_overrides.validators.EdxOAuth2Validator',
    # 3 months and then we expire refresh tokens using edx_clear_expired_tokens (length is mobile app driven)
    'REFRESH_TOKEN_EXPIRE_SECONDS': 7776000,
    'SCOPES_BACKEND_CLASS': 'openedx.core.djangoapps.oauth_dispatch.scopes.ApplicationModelScopes',
    'SCOPES': dict(OAUTH2_DEFAULT_SCOPES, **{
        'certificates:read': _('Retrieve your course certificates'),
        'grades:read': _('Retrieve your grades for your enrolled courses'),
        'tpa:read': _('Retrieve your third-party authentication username mapping'),
        # user_id is added in code as a default scope for JWT cookies and all password grant_type JWTs
        'user_id': _('Know your user identifier'),
    }),
    'DEFAULT_SCOPES': OAUTH2_DEFAULT_SCOPES,
    'REQUEST_APPROVAL_PROMPT': 'auto_even_if_expired',
    'ERROR_RESPONSE_WITH_SCOPES': True,
}
# This is required for the migrations in oauth_dispatch.models
# otherwise it fails saying this attribute is not present in Settings
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

# Automatically clean up edx-django-oauth2-provider tokens on use
OAUTH_DELETE_EXPIRED = True
OAUTH_ID_TOKEN_EXPIRATION = 60 * 60
OAUTH_ENFORCE_SECURE = True
OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS = 365
OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS = 30

################################## THIRD_PARTY_AUTH CONFIGURATION #############################
TPA_PROVIDER_BURST_THROTTLE = '10/min'
TPA_PROVIDER_SUSTAINED_THROTTLE = '50/hr'

# .. toggle_name: TPA_AUTOMATIC_LOGOUT_ENABLED
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: Redirect the user to the TPA logout URL if this flag is enabled, the
#   TPA logout URL is configured, and the user logs in through TPA.
# .. toggle_use_cases: opt_in
# .. toggle_warning: Enabling this toggle skips rendering logout.html, which is used to log the user out
#   from the different IDAs. To ensure the user is logged out of all the IDAs be sure to redirect
#   back to <LMS>/logout after logging out of the TPA.
# .. toggle_creation_date: 2023-05-07
TPA_AUTOMATIC_LOGOUT_ENABLED = False

################################## TEMPLATE CONFIGURATION #####################################
# Mako templating
import tempfile  # pylint: disable=wrong-import-position,wrong-import-order
MAKO_MODULE_DIR = os.path.join(tempfile.gettempdir(), 'mako_lms')
MAKO_TEMPLATE_DIRS_BASE = [
    PROJECT_ROOT / 'templates',
    COMMON_ROOT / 'templates',
    XMODULE_ROOT / 'capa' / 'templates',
    COMMON_ROOT / 'djangoapps' / 'pipeline_mako' / 'templates',
    OPENEDX_ROOT / 'core' / 'djangoapps' / 'cors_csrf' / 'templates',
    OPENEDX_ROOT / 'core' / 'djangoapps' / 'dark_lang' / 'templates',
    OPENEDX_ROOT / 'core' / 'lib' / 'license' / 'templates',
    OPENEDX_ROOT / 'features' / 'course_experience' / 'templates',
]


def _make_mako_template_dirs(settings):
    """
    Derives the final Mako template directories list from other settings.
    """
    if settings.ENABLE_COMPREHENSIVE_THEMING:
        themes_dirs = get_theme_base_dirs_from_settings(settings.COMPREHENSIVE_THEME_DIRS)
        for theme in get_themes_unchecked(themes_dirs, settings.PROJECT_ROOT):
            if theme.themes_base_dir not in settings.MAKO_TEMPLATE_DIRS_BASE:
                settings.MAKO_TEMPLATE_DIRS_BASE.insert(0, theme.themes_base_dir)
    return settings.MAKO_TEMPLATE_DIRS_BASE


CONTEXT_PROCESSORS = [
    'django.template.context_processors.request',
    'django.template.context_processors.static',
    'django.template.context_processors.i18n',
    'django.contrib.auth.context_processors.auth',  # this is required for admin
    'django.template.context_processors.csrf',

    # Added for django-wiki
    'django.template.context_processors.media',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',

    # Hack to get required link URLs to password reset templates
    'common.djangoapps.edxmako.shortcuts.marketing_link_context_processor',

    # Timezone processor (sends language and time_zone preference)
    'lms.djangoapps.courseware.context_processor.user_timezone_locale_prefs',

    # Online contextual help
    'help_tokens.context_processor',
    'openedx.core.djangoapps.site_configuration.context_processors.configuration_context',

    # Mobile App processor (Detects if request is from the mobile app)
    'lms.djangoapps.mobile_api.context_processor.is_from_mobile_app',

    # Context processor necessary for the survey report message appear on the admin site
    'openedx.features.survey_report.context_processors.admin_extra_context'


]

# Django templating
TEMPLATES = [
    {
        'NAME': 'django',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Don't look for template source files inside installed applications.
        'APP_DIRS': False,
        # Instead, look for template source files in these dirs.
        'DIRS': [
            PROJECT_ROOT / "templates",
            COMMON_ROOT / 'templates',
            XMODULE_ROOT / 'capa' / 'templates',
            COMMON_ROOT / 'djangoapps' / 'pipeline_mako' / 'templates',
            COMMON_ROOT / 'static',  # required to statically include common Underscore templates
        ],
        # Options specific to this backend.
        'OPTIONS': {
            'loaders': [
                # We have to use mako-aware template loaders to be able to include
                # mako templates inside django templates (such as main_django.html).
                'openedx.core.djangoapps.theming.template_loaders.ThemeTemplateLoader',
                'common.djangoapps.edxmako.makoloader.MakoFilesystemLoader',
                'common.djangoapps.edxmako.makoloader.MakoAppDirectoriesLoader',
            ],
            'context_processors': CONTEXT_PROCESSORS,
            # Change 'debug' in your environment settings files - not here.
            'debug': False
        }
    },
    {
        'NAME': 'mako',
        'BACKEND': 'common.djangoapps.edxmako.backend.Mako',
        # Don't look for template source files inside installed applications.
        'APP_DIRS': False,
        # Instead, look for template source files in these dirs.
        'DIRS': _make_mako_template_dirs,
        # Options specific to this backend.
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
            # Change 'debug' in your environment settings files - not here.
            'debug': False,
        }
    },
]
derived_collection_entry('TEMPLATES', 1, 'DIRS')
DEFAULT_TEMPLATE_ENGINE = TEMPLATES[0]
DEFAULT_TEMPLATE_ENGINE_DIRS = DEFAULT_TEMPLATE_ENGINE['DIRS'][:]

###############################################################################################

AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'bridgekeeper.backends.RulePermissionBackend',
]

STUDENT_FILEUPLOAD_MAX_SIZE = 4 * 1000 * 1000  # 4 MB
MAX_FILEUPLOADS_PER_INPUT = 20

# Set request limits for maximum size of a request body and maximum number of GET/POST parameters. (>=Django 1.10)
# Limits are currently disabled - but can be used for finer-grained denial-of-service protection.
DATA_UPLOAD_MAX_MEMORY_SIZE = None
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Configuration option for when we want to grab server error pages
STATIC_GRAB = False
DEV_CONTENT = True

# License for serving content in China
ICP_LICENSE = None
ICP_LICENSE_INFO = {}

ELASTIC_SEARCH_CONFIG = [
    {
        'use_ssl': False,
        'host': 'localhost',
        'port': 9200
    }
]

SEARCH_COURSEWARE_CONTENT_LOG_PARAMS = False


# .. setting_name: ELASTIC_SEARCH_INDEX_PREFIX
# .. setting_default: ''
# .. setting_description: Specifies the prefix used when naming elasticsearch indexes related to edx-search.
ELASTICSEARCH_INDEX_PREFIX = ""

VIDEO_CDN_URL = {
    'EXAMPLE_COUNTRY_CODE': "http://example.com/edx/video?s3_url="
}

STATIC_ROOT_BASE = '/edx/var/edxapp/staticfiles'

LOGGING_ENV = 'sandbox'

EDX_ROOT_URL = ''
EDX_API_KEY = "PUT_YOUR_API_KEY_HERE"

LOGIN_REDIRECT_URL = EDX_ROOT_URL + '/login'
LOGIN_URL = EDX_ROOT_URL + '/login'

PARTNER_SUPPORT_EMAIL = ''

CERT_QUEUE = 'certificates'

ALTERNATE_WORKER_QUEUES = 'cms'

LOCAL_LOGLEVEL = "INFO"

LOG_DIR = '/edx/var/log/edx'

DATA_DIR = '/edx/var/edxapp/data'

# .. setting_name: MAINTENANCE_BANNER_TEXT
# .. setting_default: 'Sample banner message'
# .. setting_description: Specifies the text that is rendered on the maintenance banner.
# .. setting_warning: Depends on the `open_edx_util.display_maintenance_warning` waffle switch.
#   The banner is only rendered when the switch is activated.
MAINTENANCE_BANNER_TEXT = 'Sample banner message'

DJFS = {
    'type': 'osfs',
    'directory_root': '/edx/var/edxapp/django-pyfs/static/django-pyfs',
    'url_root': '/static/django-pyfs',
}

# Set certificate issued date format. It supports all formats supported by
# `common.djangoapps.util.date_utils.strftime_localized`.
CERTIFICATE_DATE_FORMAT = "%B %-d, %Y"

### Dark code. Should be enabled in local settings for devel.

ENABLE_MULTICOURSE = False  # set to False to disable multicourse display (see lib.util.views.edXhome)

# .. toggle_name: WIKI_ENABLED
# .. toggle_implementation: DjangoSetting
# .. toggle_default: True
# .. toggle_description: This setting allows us to have a collaborative tool to contribute or
#   modify content of course related materials.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2012-07-13
WIKI_ENABLED = True

###

COURSE_MODE_DEFAULTS = {
    'android_sku': None,
    'bulk_sku': None,
    'currency': 'usd',
    'description': None,
    'expiration_datetime': None,
    'ios_sku': None,
    'min_price': 0,
    'name': _('Audit'),
    'sku': None,
    'slug': 'audit',
    'suggested_prices': '',
}

# IP addresses that are allowed to reload the course, etc.
# TODO (vshnayder): Will probably need to change as we get real access control in.
LMS_MIGRATION_ALLOWED_IPS = []

USAGE_KEY_PATTERN = r'(?P<usage_key_string>(?:i4x://?[^/]+/[^/]+/[^/]+/[^@]+(?:@[^/]+)?)|(?:[^/]+))'
ASSET_KEY_PATTERN = r'(?P<asset_key_string>(?:/?c4x(:/)?/[^/]+/[^/]+/[^/]+/[^@]+(?:@[^/]+)?)|(?:[^/]+))'
USAGE_ID_PATTERN = r'(?P<usage_id>(?:i4x://?[^/]+/[^/]+/[^/]+/[^@]+(?:@[^/]+)?)|(?:[^/]+))'


# The space is required for space-dependent languages like Arabic and Farsi.
# However, backward compatibility with Ficus older releases is still maintained (space is still not valid)
# in the AccountCreationForm and the user_api through the ENABLE_UNICODE_USERNAME feature flag.
USERNAME_REGEX_PARTIAL = r'[\w .@_+-]+'
USERNAME_PATTERN = fr'(?P<username>{USERNAME_REGEX_PARTIAL})'


############################## EVENT TRACKING #################################
LMS_SEGMENT_KEY = None

# FIXME: Should we be doing this truncation?
TRACK_MAX_EVENT = 50000

DEBUG_TRACK_LOG = False

TRACKING_BACKENDS = {
    'logger': {
        'ENGINE': 'common.djangoapps.track.backends.logger.LoggerBackend',
        'OPTIONS': {
            'name': 'tracking'
        }
    }
}

# We're already logging events, and we don't want to capture user
# names/passwords.  Heartbeat events are likely not interesting.
TRACKING_IGNORE_URL_PATTERNS = [r'^/event', r'^/login', r'^/heartbeat', r'^/segmentio/event', r'^/performance']

EVENT_TRACKING_ENABLED = True
EVENT_TRACKING_BACKENDS = {
    'tracking_logs': {
        'ENGINE': 'eventtracking.backends.routing.RoutingBackend',
        'OPTIONS': {
            'backends': {
                'logger': {
                    'ENGINE': 'eventtracking.backends.logger.LoggerBackend',
                    'OPTIONS': {
                        'name': 'tracking',
                        'max_event_size': TRACK_MAX_EVENT,
                    }
                }
            },
            'processors': [
                {'ENGINE': 'common.djangoapps.track.shim.LegacyFieldMappingProcessor'},
                {'ENGINE': 'common.djangoapps.track.shim.PrefixedEventProcessor'}
            ]
        }
    },
    'segmentio': {
        'ENGINE': 'eventtracking.backends.routing.RoutingBackend',
        'OPTIONS': {
            'backends': {
                'segment': {'ENGINE': 'eventtracking.backends.segment.SegmentBackend'}
            },
            'processors': [
                {
                    'ENGINE': 'eventtracking.processors.whitelist.NameWhitelistProcessor',
                    'OPTIONS': {
                        'whitelist': []
                    }
                },
                {
                    'ENGINE': 'common.djangoapps.track.shim.GoogleAnalyticsProcessor'
                }
            ]
        }
    }
}
EVENT_TRACKING_PROCESSORS = []
EVENT_TRACKING_SEGMENTIO_EMIT_WHITELIST = []

TRACKING_SEGMENTIO_WEBHOOK_SECRET = None
TRACKING_SEGMENTIO_ALLOWED_TYPES = ['track']
TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES = []
TRACKING_SEGMENTIO_SOURCE_MAP = {
    'analytics-android': 'mobile',
    'analytics-ios': 'mobile',
}

######################## GOOGLE ANALYTICS ###########################
GOOGLE_ANALYTICS_ACCOUNT = None
GOOGLE_SITE_VERIFICATION_ID = ''
GOOGLE_ANALYTICS_LINKEDIN = 'GOOGLE_ANALYTICS_LINKEDIN_DUMMY'
GOOGLE_ANALYTICS_TRACKING_ID = None
GOOGLE_ANALYTICS_4_ID = None

######################## BRANCH.IO ###########################
BRANCH_IO_KEY = ''

######################## OPTIMIZELY ###########################
OPTIMIZELY_PROJECT_ID = None
OPTIMIZELY_FULLSTACK_SDK_KEY = None

######################## HOTJAR ###########################
HOTJAR_SITE_ID = 00000

######################## ALGOLIA SEARCH ###########################
ALGOLIA_APP_ID = None
ALGOLIA_SEARCH_API_KEY = None

######################## subdomain specific settings ###########################
COURSE_LISTINGS = {}

############# XBlock Configuration ##########

# Import after sys.path fixup
from xmodule.modulestore.edit_info import EditInfoMixin  # lint-amnesty, pylint: disable=wrong-import-order, wrong-import-position
from xmodule.modulestore.inheritance import InheritanceMixin  # lint-amnesty, pylint: disable=wrong-import-order, wrong-import-position
from xmodule.x_module import XModuleMixin  # lint-amnesty, pylint: disable=wrong-import-order, wrong-import-position

# These are the Mixins that will be added to every Blocklike upon instantiation.
# DO NOT EXPAND THIS LIST!! We want it eventually to be EMPTY. Why? Because dynamically adding functions/behaviors to
# objects at runtime is confusing for both developers and static tooling (pylint/mypy). Instead...
#  - to add special Blocklike behaviors just for your site: override `XBLOCK_EXTRA_MIXINS` with your own XBlockMixins.
#  - to add new functionality to all Blocklikes: add it to the base Blocklike class in the core openedx/XBlock repo.
XBLOCK_MIXINS = (
    # TODO: For each of these, either
    #  (a) merge their functionality into the base Blocklike class, or
    #  (b) refactor their functionality out of the Blocklike objects and into the edx-platform block runtimes.
    LmsBlockMixin,
    InheritanceMixin,
    XModuleMixin,
    EditInfoMixin,
)

# .. setting_name: XBLOCK_EXTRA_MIXINS
# .. setting_default: ()
# .. setting_description: Custom mixins that will be dynamically added to every XBlock and XBlockAside instance.
#     These can be classes or dotted-path references to classes.
#     For example: `XBLOCK_EXTRA_MIXINS = ('my_custom_package.my_module.MyCustomMixin',)`
XBLOCK_EXTRA_MIXINS = ()

# .. setting_name: XBLOCK_FIELD_DATA_WRAPPERS
# .. setting_default: ()
# .. setting_description: Paths to wrapper methods which should be applied to every XBlock's FieldData.
XBLOCK_FIELD_DATA_WRAPPERS = ()

XBLOCK_FS_STORAGE_BUCKET = None
XBLOCK_FS_STORAGE_PREFIX = None

# .. setting_name: XBLOCK_SETTINGS
# .. setting_default: {}
# .. setting_description: Dictionary containing server-wide configuration of XBlocks on a per-type basis.
#     By default, keys should match the XBlock `block_settings_key` attribute/property. If the attribute/property
#     is not defined, use the XBlock class name. Check `xmodule.services.SettingsService`
#     for more reference.
XBLOCK_SETTINGS = {}

# .. setting_name: XBLOCK_RUNTIME_V2_EPHEMERAL_DATA_CACHE
# .. setting_default: default
# .. setting_description: The django cache key of the cache to use for storing anonymous user state for XBlocks.
XBLOCK_RUNTIME_V2_EPHEMERAL_DATA_CACHE = 'default'

############# ModuleStore Configuration ##########

MODULESTORE_BRANCH = 'published-only'

DOC_STORE_CONFIG = {
    'db': 'edxapp',
    'host': 'localhost',
    'replicaSet': '',
    'password': 'password',
    'port': 27017,
    'user': 'edxapp',
    'collection': 'modulestore',
    'ssl': False,
    # https://api.mongodb.com/python/2.9.1/api/pymongo/mongo_client.html#module-pymongo.mongo_client
    # default is never timeout while the connection is open,
    #this means it needs to explicitly close raising pymongo.errors.NetworkTimeout
    'socketTimeoutMS': 6000,
    'connectTimeoutMS': 2000,  # default is 20000, I believe raises pymongo.errors.ConnectionFailure
    # Not setting waitQueueTimeoutMS and waitQueueMultiple since pymongo defaults to nobody being allowed to wait
    'auth_source': None,
    'read_preference': 'SECONDARY_PREFERRED'
}

CONTENTSTORE = {
    'ENGINE': 'xmodule.contentstore.mongo.MongoContentStore',
    # connection strings are duplicated temporarily for
    # backward compatibility
    'OPTIONS': {
        'db': 'edxapp',
        'host': 'localhost',
        'password': 'password',
        'port': 27017,
        'user': 'edxapp',
        'ssl': False,
        'auth_source': None
    },
    'ADDITIONAL_OPTIONS': {},
    'DOC_STORE_CONFIG': DOC_STORE_CONFIG
}

MODULESTORE = {
    'default': {
        'ENGINE': 'xmodule.modulestore.mixed.MixedModuleStore',
        'OPTIONS': {
            'mappings': {},
            'stores': [
                {
                    'NAME': 'split',
                    'ENGINE': 'xmodule.modulestore.split_mongo.split_draft.DraftVersioningModuleStore',
                    'DOC_STORE_CONFIG': DOC_STORE_CONFIG,
                    'OPTIONS': {
                        'default_class': 'xmodule.hidden_block.HiddenBlock',
                        'fs_root': lambda settings: settings.DATA_DIR,
                        'render_template': 'common.djangoapps.edxmako.shortcuts.render_to_string',
                    }
                },
                {
                    'NAME': 'draft',
                    'ENGINE': 'xmodule.modulestore.mongo.DraftMongoModuleStore',
                    'DOC_STORE_CONFIG': DOC_STORE_CONFIG,
                    'OPTIONS': {
                        'default_class': 'xmodule.hidden_block.HiddenBlock',
                        'fs_root': lambda settings: settings.DATA_DIR,
                        'render_template': 'common.djangoapps.edxmako.shortcuts.render_to_string',
                    }
                }
            ]
        }
    }
}


DATABASES = {
    # edxapp's edxapp-migrate scripts and the edxapp_migrate play
    # will ensure that any DB not named read_replica will be migrated
    # for both the lms and cms.
    'default': {
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'edxapp',
        'OPTIONS': {},
        'PASSWORD': 'password',
        'PORT': '3306',
        'USER': 'edxapp001'
    },
    'read_replica': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'edxapp',
        'OPTIONS': {},
        'PASSWORD': 'password',
        'PORT': '3306',
        'USER': 'edxapp001'
    },
    'student_module_history': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'edxapp_csmh',
        'OPTIONS': {},
        'PASSWORD': 'password',
        'PORT': '3306',
        'USER': 'edxapp001'
    }
}


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DEFAULT_HASHING_ALGORITHM = 'sha256'

#################### Python sandbox ############################################

CODE_JAIL = {
    # from https://github.com/openedx/codejail/blob/master/codejail/django_integration.py#L24, '' should be same as None
    'python_bin': '/edx/app/edxapp/venvs/edxapp-sandbox/bin/python',
    # User to run as in the sandbox.
    'user': 'sandbox',

    # Configurable limits.
    'limits': {
        # How many CPU seconds can jailed code use?
        'CPU': 1,
        # Limit the memory of the jailed process to something high but not
        # infinite (512MiB in bytes)
        'VMEM': 536870912,
        # Time in seconds that the jailed process has to run.
        'REALTIME': 3,
        'PROXY': 0,
    },

    # Overrides to default configurable 'limits' (above).
    # Keys should be course run ids (or, in the special case of code running
    # on the /debug/run_python page, the key is 'debug_run_python').
    # Values should be dictionaries that look like 'limits'.
    "limit_overrides": {},
}

# Some courses are allowed to run unsafe code. This is a list of regexes, one
# of them must match the course id for that course to run unsafe code.
#
# For example:
#
#   COURSES_WITH_UNSAFE_CODE = [
#       r"Harvard/XY123.1/.*"
#   ]
COURSES_WITH_UNSAFE_CODE = []

# Code jail REST service
ENABLE_CODEJAIL_REST_SERVICE = False
# .. setting_name: CODE_JAIL_REST_SERVICE_REMOTE_EXEC
# .. setting_default: 'xmodule.capa.safe_exec.remote_exec.send_safe_exec_request_v0'
# .. setting_description: Set the python package.module.function that is reponsible of
#   calling the remote service in charge of jailed code execution
CODE_JAIL_REST_SERVICE_REMOTE_EXEC = 'xmodule.capa.safe_exec.remote_exec.send_safe_exec_request_v0'
# .. setting_name: CODE_JAIL_REST_SERVICE_HOST
# .. setting_default: 'http://127.0.0.1:8550'
# .. setting_description: Set the codejail remote service host
CODE_JAIL_REST_SERVICE_HOST = 'http://127.0.0.1:8550'
# .. setting_name: CODE_JAIL_REST_SERVICE_CONNECT_TIMEOUT
# .. setting_default: 0.5
# .. setting_description: Set the number of seconds LMS will wait to establish an internal
#   connection to the codejail remote service.
CODE_JAIL_REST_SERVICE_CONNECT_TIMEOUT = 0.5  # time in seconds
# .. setting_name: CODE_JAIL_REST_SERVICE_READ_TIMEOUT
# .. setting_default: 3.5
# .. setting_description: Set the number of seconds LMS will wait for a response from the
#   codejail remote service endpoint.
CODE_JAIL_REST_SERVICE_READ_TIMEOUT = 3.5  # time in seconds


############################### DJANGO BUILT-INS ###############################
# Change DEBUG in your environment settings files, not here
DEBUG = False
USE_TZ = True
SESSION_COOKIE_SECURE = False
SESSION_SAVE_EVERY_REQUEST = False
SESSION_SERIALIZER = 'openedx.core.lib.session_serializers.PickleSerializer'
SESSION_COOKIE_DOMAIN = ""
SESSION_COOKIE_NAME = 'sessionid'

# django-session-cookie middleware
DCS_SESSION_COOKIE_SAMESITE = 'None'
DCS_SESSION_COOKIE_SAMESITE_FORCE_ALL = True

# This is the domain that is used to set shared cookies between various sub-domains.
SHARED_COOKIE_DOMAIN = ""

# CMS base
CMS_BASE = 'localhost:18010'

# LMS base
LMS_BASE = 'localhost:18000'

# Studio name
STUDIO_NAME = 'Studio'
STUDIO_SHORT_NAME = 'Studio'

# Site info
SITE_NAME = "localhost"
HTTPS = 'on'
ROOT_URLCONF = 'lms.urls'
# NOTE: Please set ALLOWED_HOSTS to some sane value, as we do not allow the default '*'
# Platform Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'registration@example.com'
DEFAULT_FEEDBACK_EMAIL = 'feedback@example.com'
SERVER_EMAIL = 'devops@example.com'
TECH_SUPPORT_EMAIL = 'technical@example.com'
CONTACT_EMAIL = 'info@example.com'
BUGS_EMAIL = 'bugs@example.com'
UNIVERSITY_EMAIL = 'university@example.com'
PRESS_EMAIL = 'press@example.com'
FINANCE_EMAIL = ''

# Platform mailing address
CONTACT_MAILING_ADDRESS = 'SET-ME-PLEASE'

# Account activation email sender address
ACTIVATION_EMAIL_FROM_ADDRESS = ''

ADMINS = ()
MANAGERS = ADMINS

# Static content
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT_LMS', ENV_ROOT / "staticfiles")
STATIC_URL_BASE = '/static/'

STATICFILES_DIRS = [
    COMMON_ROOT / "static",
    PROJECT_ROOT / "static",
    NODE_MODULES_ROOT / "@edx",
]

FAVICON_PATH = 'images/favicon.ico'
DEFAULT_COURSE_ABOUT_IMAGE_URL = 'images/pencils.jpg'

# User-uploaded content
MEDIA_ROOT = '/edx/var/edxapp/media/'
MEDIA_URL = '/media/'

# Locale/Internationalization
CELERY_TIMEZONE = 'UTC'
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en'  # http://www.i18nguy.com/unicode/language-identifiers.html
# these languages display right to left
LANGUAGES_BIDI = ("he", "ar", "fa", "ur", "fa-ir", "rtl")

LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Sourced from http://www.localeplanet.com/icu/ and wikipedia
LANGUAGES = [
    ('en', 'English'),
    ('rtl', 'Right-to-Left Test Language'),
    ('eo', 'Dummy Language (Esperanto)'),  # Dummy languaged used for testing

    ('am', 'አማርኛ'),  # Amharic
    ('ar', 'العربية'),  # Arabic
    ('az', 'azərbaycanca'),  # Azerbaijani
    ('bg-bg', 'български (България)'),  # Bulgarian (Bulgaria)
    ('bn-bd', 'বাংলা (বাংলাদেশ)'),  # Bengali (Bangladesh)
    ('bn-in', 'বাংলা (ভারত)'),  # Bengali (India)
    ('bs', 'bosanski'),  # Bosnian
    ('ca', 'Català'),  # Catalan
    ('ca@valencia', 'Català (València)'),  # Catalan (Valencia)
    ('cs', 'Čeština'),  # Czech
    ('cy', 'Cymraeg'),  # Welsh
    ('da', 'dansk'),  # Danish
    ('de-de', 'Deutsch (Deutschland)'),  # German (Germany)
    ('el', 'Ελληνικά'),  # Greek
    ('en-uk', 'English (United Kingdom)'),  # English (United Kingdom)
    ('en@lolcat', 'LOLCAT English'),  # LOLCAT English
    ('en@pirate', 'Pirate English'),  # Pirate English
    ('es-419', 'Español (Latinoamérica)'),  # Spanish (Latin America)
    ('es-ar', 'Español (Argentina)'),  # Spanish (Argentina)
    ('es-ec', 'Español (Ecuador)'),  # Spanish (Ecuador)
    ('es-es', 'Español (España)'),  # Spanish (Spain)
    ('es-mx', 'Español (México)'),  # Spanish (Mexico)
    ('es-pe', 'Español (Perú)'),  # Spanish (Peru)
    ('et-ee', 'Eesti (Eesti)'),  # Estonian (Estonia)
    ('eu-es', 'euskara (Espainia)'),  # Basque (Spain)
    ('fa', 'فارسی'),  # Persian
    ('fa-ir', 'فارسی (ایران)'),  # Persian (Iran)
    ('fi-fi', 'Suomi (Suomi)'),  # Finnish (Finland)
    ('fil', 'Filipino'),  # Filipino
    ('fr', 'Français'),  # French
    ('gl', 'Galego'),  # Galician
    ('gu', 'ગુજરાતી'),  # Gujarati
    ('he', 'עברית'),  # Hebrew
    ('hi', 'हिन्दी'),  # Hindi
    ('hr', 'hrvatski'),  # Croatian
    ('hu', 'magyar'),  # Hungarian
    ('hy-am', 'Հայերեն (Հայաստան)'),  # Armenian (Armenia)
    ('id', 'Bahasa Indonesia'),  # Indonesian
    ('it-it', 'Italiano (Italia)'),  # Italian (Italy)
    ('ja-jp', '日本語 (日本)'),  # Japanese (Japan)
    ('kk-kz', 'қазақ тілі (Қазақстан)'),  # Kazakh (Kazakhstan)
    ('km-kh', 'ភាសាខ្មែរ (កម្ពុជា)'),  # Khmer (Cambodia)
    ('kn', 'ಕನ್ನಡ'),  # Kannada
    ('ko-kr', '한국어 (대한민국)'),  # Korean (Korea)
    ('lt-lt', 'Lietuvių (Lietuva)'),  # Lithuanian (Lithuania)
    ('ml', 'മലയാളം'),  # Malayalam
    ('mn', 'Монгол хэл'),  # Mongolian
    ('mr', 'मराठी'),  # Marathi
    ('ms', 'Bahasa Melayu'),  # Malay
    ('nb', 'Norsk bokmål'),  # Norwegian Bokmål
    ('ne', 'नेपाली'),  # Nepali
    ('nl-nl', 'Nederlands (Nederland)'),  # Dutch (Netherlands)
    ('or', 'ଓଡ଼ିଆ'),  # Oriya
    ('pl', 'Polski'),  # Polish
    ('pt-br', 'Português (Brasil)'),  # Portuguese (Brazil)
    ('pt-pt', 'Português (Portugal)'),  # Portuguese (Portugal)
    ('ro', 'română'),  # Romanian
    ('ru', 'Русский'),  # Russian
    ('si', 'සිංහල'),  # Sinhala
    ('sk', 'Slovenčina'),  # Slovak
    ('sl', 'Slovenščina'),  # Slovenian
    ('sq', 'shqip'),  # Albanian
    ('sr', 'Српски'),  # Serbian
    ('sv', 'svenska'),  # Swedish
    ('sw', 'Kiswahili'),  # Swahili
    ('ta', 'தமிழ்'),  # Tamil
    ('te', 'తెలుగు'),  # Telugu
    ('th', 'ไทย'),  # Thai
    ('tr-tr', 'Türkçe (Türkiye)'),  # Turkish (Turkey)
    ('uk', 'Українська'),  # Ukranian
    ('ur', 'اردو'),  # Urdu
    ('vi', 'Tiếng Việt'),  # Vietnamese
    ('uz', 'Ўзбек'),  # Uzbek
    ('zh-cn', '中文 (简体)'),  # Chinese (China)
    ('zh-hk', '中文 (香港)'),  # Chinese (Hong Kong)
    ('zh-tw', '中文 (台灣)'),  # Chinese (Taiwan)
]

LANGUAGE_DICT = dict(LANGUAGES)

# Languages supported for custom course certificate templates
CERTIFICATE_TEMPLATE_LANGUAGES = {
    'en': 'English',
    'es': 'Español',
}

USE_I18N = True
USE_L10N = True

STATICI18N_FILENAME_FUNCTION = 'statici18n.utils.legacy_filename'
STATICI18N_ROOT = PROJECT_ROOT / "static"
STATICI18N_OUTPUT_DIR = "js/i18n"


# Localization strings (e.g. django.po) are under these directories
def _make_locale_paths(settings):  # pylint: disable=missing-function-docstring
    locale_paths = list(settings.PREPEND_LOCALE_PATHS)
    locale_paths += [settings.REPO_ROOT + '/conf/locale']  # edx-platform/conf/locale/

    if settings.ENABLE_COMPREHENSIVE_THEMING:
        # Add locale paths to settings for comprehensive theming.
        for locale_path in settings.COMPREHENSIVE_THEME_LOCALE_PATHS:
            locale_paths += (path(locale_path), )
    return locale_paths
LOCALE_PATHS = _make_locale_paths
derived('LOCALE_PATHS')

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Guidelines for translators
TRANSLATORS_GUIDE = 'https://edx.readthedocs.org/projects/edx-developer-guide/en/latest/' \
                    'conventions/internationalization/i18n_translators_guide.html'

#################################### AWS #######################################
# The number of seconds that a generated URL is valid for.
AWS_QUERYSTRING_EXPIRE = 10 * 365 * 24 * 60 * 60  # 10 years
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = "SET-ME-PLEASE (ex. bucket-name)"
AWS_S3_CUSTOM_DOMAIN = "SET-ME-PLEASE (ex. bucket-name.s3.amazonaws.com)"

################################# SIMPLEWIKI ###################################
SIMPLE_WIKI_REQUIRE_LOGIN_EDIT = True
SIMPLE_WIKI_REQUIRE_LOGIN_VIEW = False

################################# WIKI ###################################
from lms.djangoapps.course_wiki import settings as course_wiki_settings  # pylint: disable=wrong-import-position

# .. toggle_name: WIKI_ACCOUNT_HANDLING
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: We recommend you leave this as 'False' for an Open edX installation
#   to get the proper behavior for register, login and logout. For the original docs see:
#   https://github.com/openedx/django-wiki/blob/edx_release/wiki/conf/settings.py
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2012-08-13
WIKI_ACCOUNT_HANDLING = False
WIKI_EDITOR = 'lms.djangoapps.course_wiki.editors.CodeMirror'
WIKI_SHOW_MAX_CHILDREN = 0  # We don't use the little menu that shows children of an article in the breadcrumb
# .. toggle_name: WIKI_ANONYMOUS
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: Enabling this allows access to anonymous users.
#   For the original docs, see:
#   https://github.com/openedx/django-wiki/blob/edx_release/wiki/conf/settings.py
# .. toggle_warning: Setting allow anonymous access to `True` may have styling issues.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2012-08-21
WIKI_ANONYMOUS = False

WIKI_CAN_DELETE = course_wiki_settings.CAN_DELETE
WIKI_CAN_MODERATE = course_wiki_settings.CAN_MODERATE
WIKI_CAN_CHANGE_PERMISSIONS = course_wiki_settings.CAN_CHANGE_PERMISSIONS
WIKI_CAN_ASSIGN = course_wiki_settings.CAN_ASSIGN
# .. toggle_name: WIKI_USE_BOOTSTRAP_SELECT_WIDGET
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: Enabling this will use the bootstrap select widget.
#   For the original docs, see:
#   https://github.com/openedx/django-wiki/blob/edx_release/wiki/conf/settings.py
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2012-08-22
WIKI_USE_BOOTSTRAP_SELECT_WIDGET = False
# .. toggle_name: WIKI_LINK_LIVE_LOOKUPS
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: This setting is defined in the original docs:
#   https://github.com/openedx/django-wiki/blob/edx_release/wiki/conf/settings.py
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2012-08-23
WIKI_LINK_LIVE_LOOKUPS = False
WIKI_LINK_DEFAULT_LEVEL = 2

##### Zendesk #####
ZENDESK_URL = ''
ZENDESK_USER = ''
ZENDESK_API_KEY = ''
ZENDESK_CUSTOM_FIELDS = {}
ZENDESK_OAUTH_ACCESS_TOKEN = ''
# A mapping of string names to Zendesk Group IDs
# To get the IDs of your groups you can go to
# {zendesk_url}/api/v2/groups.json
ZENDESK_GROUP_ID_MAPPING = {}

##### EMBARGO #####
EMBARGO_SITE_REDIRECT_URL = None

##### shoppingcart Payment #####
PAYMENT_SUPPORT_EMAIL = 'billing@example.com'

# Setting for PAID_COURSE_REGISTRATION, DOES NOT AFFECT VERIFIED STUDENTS
PAID_COURSE_REGISTRATION_CURRENCY = ['usd', '$']

################################# EdxNotes config  #########################

# Configure the LMS to use our stub EdxNotes implementation
# .. setting_name: EDXNOTES_PUBLIC_API
# .. setting_default: http://localhost:18120/api/v1
# .. setting_description: Set the public API endpoint LMS will use in the frontend to
#     interact with the edx_notes_api service.
# .. setting_warning: This setting must be a publicly accessible endpoint. It is only used
#     when the setting FEATURES['ENABLE_EDXNOTES'] is activated.
EDXNOTES_PUBLIC_API = 'http://localhost:18120/api/v1'
# .. setting_name: EDXNOTES_INTERNAL_API
# .. setting_default: http://localhost:18120/api/v1
# .. setting_description: Set the internal API endpoint LMS will use in the backend to
#     interact with the edx_notes_api service.
# .. setting_warning: Normally set to the same value of EDXNOTES_PUBLIC_API. It is not
#     mandatory for this setting to be a publicly accessible endpoint, but to be accessible
#     by the LMS service. It is only used when the setting FEATURES['ENABLE_EDXNOTES'] is
#     activated.
EDXNOTES_INTERNAL_API = 'http://localhost:18120/api/v1'
# .. setting_name: EDXNOTES_CLIENT_NAME
# .. setting_default: edx-notes
# .. setting_description: Set the name of the Oauth client used by LMS to authenticate with
#     the edx_notes_api service.
# .. setting_warning: The Oauth client must be created in the platform Django admin in the
#     path /admin/oauth2_provider/application/, setting the name field of the client as the
#     value of this setting.
EDXNOTES_CLIENT_NAME = "edx-notes"
# .. setting_name: EDXNOTES_CONNECT_TIMEOUT
# .. setting_default: 0.5
# .. setting_description: Set the number of seconds LMS will wait to establish an internal
#     connection to the edx_notes_api service.
EDXNOTES_CONNECT_TIMEOUT = 0.5  # time in seconds
# .. setting_name: EDXNOTES_READ_TIMEOUT
# .. setting_default: 1.5
# .. setting_description: Set the number of seconds LMS will wait for a response from the
#     edx_notes_api service internal endpoint.
EDXNOTES_READ_TIMEOUT = 1.5  # time in seconds

########################## Parental controls config  #######################

# The age at which a learner no longer requires parental consent, or None
# if parental consent is never required.
PARENTAL_CONSENT_AGE_LIMIT = 13

######################### Branded Footer ###################################
# Constants for the footer used on the site and shared with other sites
# (such as marketing and the blog) via the branding API.

# URL for Open edX displayed in the footer
FOOTER_OPENEDX_URL = "https://open.edx.org"

# URL for the OpenEdX logo image
# We use logo images served from files.edx.org so we can (roughly) track
# how many OpenEdX installations are running.
# Site operators can choose from these logo options:
# * https://logos.openedx.org/open-edx-logo-tag.png
# * https://logos.openedx.org/open-edx-logo-tag-light.png"
# * https://logos.openedx.org/open-edx-logo-tag-dark.png
FOOTER_OPENEDX_LOGO_IMAGE = "https://logos.openedx.org/open-edx-logo-tag.png"

# These are referred to both by the Django asset pipeline
# AND by the branding footer API, which needs to decide which
# version of the CSS to serve.
FOOTER_CSS = {
    "openedx": {
        "ltr": "style-lms-footer",
        "rtl": "style-lms-footer-rtl",
    },
    "edx": {
        "ltr": "style-lms-footer-edx",
        "rtl": "style-lms-footer-edx-rtl",
    },
}

# Cache expiration for the version of the footer served
# by the branding API.
FOOTER_CACHE_TIMEOUT = 30 * 60

# Max age cache control header for the footer (controls browser caching).
FOOTER_BROWSER_CACHE_MAX_AGE = 5 * 60

# Credit api notification cache timeout
CREDIT_NOTIFICATION_CACHE_TIMEOUT = 5 * 60 * 60

################################# Middleware ###################################

MIDDLEWARE = [
    'openedx.core.lib.x_forwarded_for.middleware.XForwardedForMiddleware',
    'edx_django_utils.security.csp.middleware.content_security_policy_middleware',

    'crum.CurrentRequestUserMiddleware',

    # Resets the request cache.
    'edx_django_utils.cache.middleware.RequestCacheMiddleware',

    # Various monitoring middleware
    'edx_django_utils.monitoring.CachedCustomMonitoringMiddleware',
    'edx_django_utils.monitoring.CodeOwnerMonitoringMiddleware',
    'edx_django_utils.monitoring.CookieMonitoringMiddleware',
    'edx_django_utils.monitoring.DeploymentMonitoringMiddleware',
    'edx_django_utils.monitoring.FrontendMonitoringMiddleware',

    # Before anything that looks at cookies, especially the session middleware
    'openedx.core.djangoapps.cookie_metadata.middleware.CookieNameChange',

    # Monitoring and logging for ignored errors
    'openedx.core.lib.request_utils.IgnoredErrorMiddleware',

    'lms.djangoapps.mobile_api.middleware.AppVersionUpgrade',
    'openedx.core.djangoapps.header_control.middleware.HeaderControlMiddleware',
    'lms.djangoapps.discussion.django_comment_client.middleware.AjaxExceptionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'edx_rest_framework_extensions.auth.jwt.middleware.JwtAuthCookieMiddleware',

    # Allows us to define redirects via Django admin
    'django_sites_extensions.middleware.RedirectMiddleware',

    # Instead of SessionMiddleware, we use a more secure version
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'openedx.core.djangoapps.safe_sessions.middleware.SafeSessionMiddleware',

    # Instead of AuthenticationMiddleware, we use a cached backed version
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openedx.core.djangoapps.cache_toolbox.middleware.CacheBackedAuthenticationMiddleware',

    # Middleware to flush user's session in other browsers when their email is changed.
    'openedx.core.djangoapps.safe_sessions.middleware.EmailChangeMiddleware',

    'common.djangoapps.student.middleware.UserStandingMiddleware',
    'openedx.core.djangoapps.contentserver.middleware.StaticContentServerMiddleware',

    # Adds user tags to tracking events
    # Must go before TrackMiddleware, to get the context set up
    'openedx.core.djangoapps.user_api.middleware.UserTagsEventContextMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'common.djangoapps.track.middleware.TrackMiddleware',

    # CORS and CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'openedx.core.djangoapps.cors_csrf.middleware.CorsCSRFMiddleware',
    'openedx.core.djangoapps.cors_csrf.middleware.CsrfCrossDomainCookieMiddleware',

    'openedx.core.djangoapps.geoinfo.middleware.CountryMiddleware',
    'openedx.core.djangoapps.embargo.middleware.EmbargoMiddleware',

    # Allows us to use enterprise customer's language as the learner's default language
    # This middleware must come before `LanguagePreferenceMiddleware` middleware
    'enterprise.middleware.EnterpriseLanguagePreferenceMiddleware',

    # Allows us to set user preferences
    'openedx.core.djangoapps.lang_pref.middleware.LanguagePreferenceMiddleware',

    # Allows us to dark-launch particular languages.
    # Must be after LangPrefMiddleware, so ?preview-lang query params can override
    # user's language preference. ?clear-lang resets to user's language preference.
    'openedx.core.djangoapps.dark_lang.middleware.DarkLangMiddleware',

    # Detects user-requested locale from 'accept-language' header in http request.
    # Must be after DarkLangMiddleware.
    'django.middleware.locale.LocaleMiddleware',

    'lms.djangoapps.discussion.django_comment_client.utils.ViewNameMiddleware',
    'codejail.django_integration.ConfigureCodeJailMiddleware',

    # for expiring inactive sessions
    'openedx.core.djangoapps.session_inactivity_timeout.middleware.SessionInactivityTimeout',

    # use Django built in clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # to redirected unenrolled students to the course info page
    'lms.djangoapps.courseware.middleware.CacheCourseIdMiddleware',
    'lms.djangoapps.courseware.middleware.RedirectMiddleware',

    'lms.djangoapps.course_wiki.middleware.WikiAccessMiddleware',

    'openedx.core.djangoapps.theming.middleware.CurrentSiteThemeMiddleware',

    'waffle.middleware.WaffleMiddleware',

    # Enables force_django_cache_miss functionality for TieredCache.
    'edx_django_utils.cache.middleware.TieredCacheMiddleware',

    # Adds monitoring attributes to requests.
    'edx_rest_framework_extensions.middleware.RequestCustomAttributesMiddleware',

    'edx_rest_framework_extensions.auth.jwt.middleware.EnsureJWTAuthSettingsMiddleware',

    # Handles automatically storing user ids in django-simple-history tables when possible.
    'simple_history.middleware.HistoryRequestMiddleware',

    # This must be last
    'openedx.core.djangoapps.site_configuration.middleware.SessionCookieDomainOverrideMiddleware',
]

# Clickjacking protection can be disbaled by setting this to 'ALLOW'
X_FRAME_OPTIONS = 'DENY'

# Platform for Privacy Preferences header
P3P_HEADER = 'CP="Open EdX does not have a P3P policy."'

############################### PIPELINE #######################################

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    # Don't wrap JavaScript as there is code that depends upon updating the global namespace
    'DISABLE_WRAPPER': True,
    # Specify the UglifyJS binary to use
    'UGLIFYJS_BINARY': 'node_modules/.bin/uglifyjs',
}

STATICFILES_STORAGE = 'openedx.core.storage.ProductionStorage'
STATICFILES_STORAGE_KWARGS = {}

# List of finder classes that know how to find static files in various locations.
# Note: the pipeline finder is included to be able to discover optimized files
STATICFILES_FINDERS = [
    'openedx.core.djangoapps.theming.finders.ThemeFilesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openedx.core.lib.xblock_pipeline.finder.XBlockPipelineFinder',
    'pipeline.finders.PipelineFinder',
]

from openedx.core.lib.rooted_paths import rooted_glob  # pylint: disable=wrong-import-position

courseware_js = [
    'js/ajax-error.js',
    'js/courseware.js',
    'js/histogram.js',
    'js/navigation.js',
    'js/modules/tab.js',
]


# Before a student accesses courseware, we do not
# need many of the JS dependencies.  This includes
# only the dependencies used everywhere in the LMS
# (including the dashboard/account/profile pages)
# Currently, this partially duplicates the "main vendor"
# JavaScript file, so only one of the two should be included
# on a page at any time.
# In the future, we will likely refactor this to use
# RequireJS and an optimizer.
base_vendor_js = [
    'common/js/vendor/jquery.js',
    'common/js/vendor/jquery-migrate.js',
    'js/vendor/jquery.cookie.js',
    'js/vendor/url.min.js',
    'common/js/vendor/underscore.js',
    'common/js/vendor/underscore.string.js',
    'common/js/vendor/picturefill.js',

    # Make some edX UI Toolkit utilities available in the global "edx" namespace
    'edx-ui-toolkit/js/utils/global-loader.js',
    'edx-ui-toolkit/js/utils/string-utils.js',
    'edx-ui-toolkit/js/utils/html-utils.js',

    # Finally load RequireJS and dependent vendor libraries
    'common/js/vendor/require.js',
    'js/RequireJS-namespace-undefine.js',
    'js/vendor/URI.min.js',
    'common/js/vendor/backbone.js'
]

main_vendor_js = base_vendor_js + [
    'js/vendor/json2.js',
    'js/vendor/jquery-ui.min.js',
    'js/vendor/jquery.qtip.min.js',
    'js/vendor/jquery.ba-bbq.min.js',
]

# Common files used by both RequireJS code and non-RequireJS code
base_application_js = [
    'js/src/utility.js',
    'js/src/logger.js',
    'js/user_dropdown_v1.js',  # Custom dropdown keyboard handling for legacy pages
    'js/dialog_tab_controls.js',
    'js/src/string_utils.js',
    'js/form.ext.js',
    'js/src/ie_shim.js',
    'js/src/accessibility_tools.js',
    'js/toggle_login_modal.js',
    'js/src/lang_edx.js',
]

dashboard_js = (
    sorted(rooted_glob(PROJECT_ROOT / 'static', 'js/dashboard/**/*.js'))
)
discussion_js = (
    rooted_glob(PROJECT_ROOT / 'static', 'js/customwmd.js') +
    rooted_glob(PROJECT_ROOT / 'static', 'js/mathjax_accessible.js') +
    rooted_glob(PROJECT_ROOT / 'static', 'js/mathjax_delay_renderer.js') +
    sorted(rooted_glob(COMMON_ROOT / 'static', 'common/js/discussion/**/*.js'))
)

discussion_vendor_js = [
    'js/Markdown.Converter.js',
    'js/Markdown.Sanitizer.js',
    'js/Markdown.Editor.js',
    'js/vendor/jquery.timeago.js',
    'js/src/jquery.timeago.locale.js',
    'js/vendor/jquery.truncate.js',
    'js/jquery.ajaxfileupload.js',
    'js/split.js'
]

instructor_dash_js = sorted(rooted_glob(PROJECT_ROOT / 'static', 'js/instructor_dashboard/**/*.js'))

verify_student_js = [
    'js/sticky_filter.js',
    'js/query-params.js',
    'js/verify_student/models/verification_model.js',
    'js/verify_student/views/error_view.js',
    'js/verify_student/views/image_input_view.js',
    'js/verify_student/views/webcam_photo_view.js',
    'js/verify_student/views/step_view.js',
    'js/verify_student/views/intro_step_view.js',
    'js/verify_student/views/make_payment_step_view.js',
    'js/verify_student/views/face_photo_step_view.js',
    'js/verify_student/views/id_photo_step_view.js',
    'js/verify_student/views/review_photos_step_view.js',
    'js/verify_student/views/enrollment_confirmation_step_view.js',
    'js/verify_student/views/pay_and_verify_view.js',
    'js/verify_student/pay_and_verify.js',
]

reverify_js = [
    'js/verify_student/views/error_view.js',
    'js/verify_student/views/image_input_view.js',
    'js/verify_student/views/webcam_photo_view.js',
    'js/verify_student/views/step_view.js',
    'js/verify_student/views/face_photo_step_view.js',
    'js/verify_student/views/id_photo_step_view.js',
    'js/verify_student/views/review_photos_step_view.js',
    'js/verify_student/views/reverify_success_step_view.js',
    'js/verify_student/models/verification_model.js',
    'js/verify_student/views/reverify_view.js',
    'js/verify_student/reverify.js',
]

incourse_reverify_js = [
    'js/verify_student/views/error_view.js',
    'js/verify_student/views/image_input_view.js',
    'js/verify_student/views/webcam_photo_view.js',
    'js/verify_student/models/verification_model.js',
    'js/verify_student/views/incourse_reverify_view.js',
    'js/verify_student/incourse_reverify.js',
]

ccx_js = sorted(rooted_glob(PROJECT_ROOT / 'static', 'js/ccx/**/*.js'))

certificates_web_view_js = [
    'common/js/vendor/jquery.js',
    'common/js/vendor/jquery-migrate.js',
    'js/vendor/jquery.cookie.js',
    'js/src/logger.js',
    'js/utils/facebook.js',
]

credit_web_view_js = [
    'common/js/vendor/jquery.js',
    'common/js/vendor/jquery-migrate.js',
    'js/vendor/jquery.cookie.js',
    'js/src/logger.js',
]

PIPELINE['STYLESHEETS'] = {
    'style-vendor': {
        'source_filenames': [
            'css/vendor/font-awesome.css',
            'css/vendor/jquery.qtip.min.css',
        ],
        'output_filename': 'css/lms-style-vendor.css',
    },
    'style-vendor-tinymce-content': {
        'source_filenames': [
            'js/vendor/tinymce/js/tinymce/skins/ui/studio-tmce5/content.min.css'
        ],
        'output_filename': 'css/lms-style-vendor-tinymce-content.css',
    },
    'style-vendor-tinymce-skin': {
        'source_filenames': [
            'js/vendor/tinymce/js/tinymce/skins/ui/studio-tmce5/skin.min.css'
        ],
        'output_filename': 'css/lms-style-vendor-tinymce-skin.css',
    },
    'style-main-v1': {
        'source_filenames': [
            'css/lms-main-v1.css',
        ],
        'output_filename': 'css/lms-main-v1.css',
    },
    'style-main-v1-rtl': {
        'source_filenames': [
            'css/lms-main-v1-rtl.css',
        ],
        'output_filename': 'css/lms-main-v1-rtl.css',
    },
    'style-course-vendor': {
        'source_filenames': [
            'js/vendor/CodeMirror/codemirror.css',
            'css/vendor/jquery.treeview.css',
            'css/vendor/ui-lightness/jquery-ui-1.8.22.custom.css',
        ],
        'output_filename': 'css/lms-style-course-vendor.css',
    },
    'style-course': {
        'source_filenames': [
            'css/lms-course.css',
        ],
        'output_filename': 'css/lms-course.css',
    },
    'style-course-rtl': {
        'source_filenames': [
            'css/lms-course-rtl.css',
        ],
        'output_filename': 'css/lms-course-rtl.css',
    },
    'style-student-notes': {
        'source_filenames': [
            'css/vendor/edxnotes/annotator.min.css',
        ],
        'output_filename': 'css/lms-style-student-notes.css',
    },
    'style-inline-discussion': {
        'source_filenames': [
            'css/discussion/inline-discussion.css',
        ],
        'output_filename': 'css/discussion/inline-discussion.css',
    },
    'style-inline-discussion-rtl': {
        'source_filenames': [
            'css/discussion/inline-discussion-rtl.css',
        ],
        'output_filename': 'css/discussion/inline-discussion-rtl.css',
    },
    FOOTER_CSS['openedx']['ltr']: {
        'source_filenames': [
            'css/lms-footer.css',
        ],
        'output_filename': 'css/lms-footer.css',
    },
    FOOTER_CSS['openedx']['rtl']: {
        'source_filenames': [
            'css/lms-footer-rtl.css',
        ],
        'output_filename': 'css/lms-footer-rtl.css'
    },
    FOOTER_CSS['edx']['ltr']: {
        'source_filenames': [
            'css/lms-footer-edx.css',
        ],
        'output_filename': 'css/lms-footer-edx.css'
    },
    FOOTER_CSS['edx']['rtl']: {
        'source_filenames': [
            'css/lms-footer-edx-rtl.css',
        ],
        'output_filename': 'css/lms-footer-edx-rtl.css'
    },
    'style-certificates': {
        'source_filenames': [
            'certificates/css/main-ltr.css',
            'css/vendor/font-awesome.css',
        ],
        'output_filename': 'css/certificates-style.css'
    },
    'style-certificates-rtl': {
        'source_filenames': [
            'certificates/css/main-rtl.css',
            'css/vendor/font-awesome.css',
        ],
        'output_filename': 'css/certificates-style-rtl.css'
    },
    'style-mobile': {
        'source_filenames': [
            'css/lms-mobile.css',
        ],
        'output_filename': 'css/lms-mobile.css',
    },
    'style-mobile-rtl': {
        'source_filenames': [
            'css/lms-mobile-rtl.css',
        ],
        'output_filename': 'css/lms-mobile-rtl.css',
    },
}

common_js = [
    'js/src/ajax_prefix.js',
    'js/src/jquery.immediateDescendents.js',
    'js/src/xproblem.js',
]
xblock_runtime_js = [
    'common/js/xblock/core.js',
    'common/js/xblock/runtime.v1.js',
    'lms/js/xblock/lms.runtime.v1.js',
]
lms_application_js = [
    'js/calculator.js',
    'js/feedback_form.js',
    'js/main.js',
]

PIPELINE['JAVASCRIPT'] = {
    'base_application': {
        'source_filenames': base_application_js,
        'output_filename': 'js/lms-base-application.js',
    },
    'application': {
        'source_filenames': (
            common_js + xblock_runtime_js + base_application_js + lms_application_js +
            [
                'js/sticky_filter.js',
                'js/query-params.js',
                'common/js/vendor/moment-with-locales.js',
                'common/js/vendor/moment-timezone-with-data.js',
            ]
        ),
        'output_filename': 'js/lms-application.js',
    },
    'courseware': {
        'source_filenames': courseware_js,
        'output_filename': 'js/lms-courseware.js',
    },
    'base_vendor': {
        'source_filenames': base_vendor_js,
        'output_filename': 'js/lms-base-vendor.js',
    },
    'main_vendor': {
        'source_filenames': main_vendor_js,
        'output_filename': 'js/lms-main_vendor.js',
    },
    'discussion': {
        'source_filenames': discussion_js,
        'output_filename': 'js/discussion.js',
    },
    'discussion_vendor': {
        'source_filenames': discussion_vendor_js,
        'output_filename': 'js/discussion_vendor.js',
    },
    'instructor_dash': {
        'source_filenames': instructor_dash_js,
        'output_filename': 'js/instructor_dash.js',
    },
    'dashboard': {
        'source_filenames': dashboard_js,
        'output_filename': 'js/dashboard.js'
    },
    'verify_student': {
        'source_filenames': verify_student_js,
        'output_filename': 'js/verify_student.js'
    },
    'reverify': {
        'source_filenames': reverify_js,
        'output_filename': 'js/reverify.js'
    },
    'incourse_reverify': {
        'source_filenames': incourse_reverify_js,
        'output_filename': 'js/incourse_reverify.js'
    },
    'ccx': {
        'source_filenames': ccx_js,
        'output_filename': 'js/ccx.js'
    },
    'footer_edx': {
        'source_filenames': ['js/footer-edx.js'],
        'output_filename': 'js/footer-edx.js'
    },
    'certificates_wv': {
        'source_filenames': certificates_web_view_js,
        'output_filename': 'js/certificates/web_view.js'
    },
    'credit_wv': {
        'source_filenames': credit_web_view_js,
        'output_filename': 'js/credit/web_view.js'
    }
}


STATICFILES_IGNORE_PATTERNS = (
    "*.py",
    "*.pyc",

    # It would be nice if we could do, for example, "**/*.scss",
    # but these strings get passed down to the `fnmatch` module,
    # which doesn't support that. :(
    # http://docs.python.org/2/library/fnmatch.html
    "sass/*.scss",
    "sass/*/*.scss",
    "sass/*/*/*.scss",
    "sass/*/*/*/*.scss",

    # Ignore tests
    "spec",
    "spec_helpers",

    # Symlinks used by js-test-tool
    "xmodule_js",
)


################################# DJANGO-REQUIRE ###############################

# The baseUrl to pass to the r.js optimizer, relative to STATIC_ROOT.
REQUIRE_BASE_URL = "./"

# The name of a build profile to use for your project, relative to REQUIRE_BASE_URL.
# A sensible value would be 'app.build.js'. Leave blank to use the built-in default build profile.
# Set to False to disable running the default profile (e.g. if only using it to build Standalone
# Modules)
REQUIRE_BUILD_PROFILE = "lms/js/build.js"

# The name of the require.js script used by your project, relative to REQUIRE_BASE_URL.
REQUIRE_JS = "common/js/vendor/require.js"

# Whether to run django-require in debug mode.
REQUIRE_DEBUG = False

# In production, the Django pipeline appends a file hash to JavaScript file names.
# This makes it difficult for RequireJS to load its requirements, since module names
# specified in JavaScript code do not include the hash.
# For this reason, we calculate the actual path including the hash on the server
# when rendering the page.  We then override the default paths provided to RequireJS
# so it can resolve the module name to the correct URL.
#
# If you want to load JavaScript dependencies using RequireJS
# but you don't want to include those dependencies in the JS bundle for the page,
# then you need to add the js urls in this list.
REQUIRE_JS_PATH_OVERRIDES = {
    'course_bookmarks/js/views/bookmark_button': 'course_bookmarks/js/views/bookmark_button.js',
    'js/views/message_banner': 'js/views/message_banner.js',
    'moment': 'common/js/vendor/moment-with-locales.js',
    'moment-timezone': 'common/js/vendor/moment-timezone-with-data.js',
    'js/courseware/course_info_events': 'js/courseware/course_info_events.js',
    'js/courseware/accordion_events': 'js/courseware/accordion_events.js',
    'js/dateutil_factory': 'js/dateutil_factory.js',
    'js/courseware/link_clicked_events': 'js/courseware/link_clicked_events.js',
    'js/courseware/toggle_element_visibility': 'js/courseware/toggle_element_visibility.js',
    'js/student_account/logistration_factory': 'js/student_account/logistration_factory.js',
    'js/courseware/courseware_factory': 'js/courseware/courseware_factory.js',
    'js/groups/views/cohorts_dashboard_factory': 'js/groups/views/cohorts_dashboard_factory.js',
    'js/groups/discussions_management/discussions_dashboard_factory':
        'js/discussions_management/views/discussions_dashboard_factory.js',
    'draggabilly': 'js/vendor/draggabilly.js',
    'hls': 'common/js/vendor/hls.js'
}

########################## DJANGO WEBPACK LOADER ##############################

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(STATIC_ROOT, 'webpack-stats.json'),
    },
    'WORKERS': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(STATIC_ROOT, 'webpack-worker-stats.json')
    }
}

# .. setting_name: WEBPACK_CONFIG_PATH
# .. setting_default: "webpack.prod.config.js"
# .. setting_description: Path to the Webpack configuration file. Used by Paver scripts.
# .. setting_warning: This Django setting is DEPRECATED! Starting in Sumac, Webpack will no longer
#   use Django settings. Please set the WEBPACK_CONFIG_PATH environment variable instead. For details,
#   see: https://github.com/openedx/edx-platform/issues/31895
WEBPACK_CONFIG_PATH = os.environ.get('WEBPACK_CONFIG_PATH', 'webpack.prod.config.js')

########################## DJANGO DEBUG TOOLBAR ###############################

# We don't enable Django Debug Toolbar universally, but whenever we do, we want
# to avoid patching settings.  Patched settings can cause circular import
# problems: https://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup

DEBUG_TOOLBAR_PATCH_SETTINGS = False

################################# CELERY ######################################

CELERY_IMPORTS = [
    # Since xblock-poll is not a Django app, and XBlocks don't get auto-imported
    # by celery workers, its tasks will not get auto-discovered:
    'poll.tasks',
]

# .. setting_name: CELERY_EXTRA_IMPORTS
# .. setting_default: []
# .. setting_description: Adds extra packages that don't get auto-imported (Example: XBlocks).
#    These packages are added in addition to those added by CELERY_IMPORTS.
CELERY_EXTRA_IMPORTS = []

# Message configuration

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_MESSAGE_COMPRESSION = 'gzip'

# Results configuration

CELERY_IGNORE_RESULT = False
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

# Events configuration

CELERY_TRACK_STARTED = True

CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True

# Exchange configuration

CELERY_DEFAULT_EXCHANGE = 'edx.core'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'


# SERVICE_VARIANT specifies name of the variant used, which decides what JSON
# configuration files are read during startup.
SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', "lms")

# CONFIG_PREFIX specifies the prefix of the JSON configuration files,
# based on the service variant. If no variant is use, don't use a
# prefix.
CONFIG_PREFIX = SERVICE_VARIANT + "." if SERVICE_VARIANT else ""

# Queues configuration

# Name the exchange and queues w.r.t the SERVICE_VARIANT
QUEUE_VARIANT = CONFIG_PREFIX.lower()

CELERY_DEFAULT_EXCHANGE = f'edx.{QUEUE_VARIANT}core'

HIGH_PRIORITY_QUEUE = f'edx.{QUEUE_VARIANT}core.high'
DEFAULT_PRIORITY_QUEUE = f'edx.{QUEUE_VARIANT}core.default'
HIGH_MEM_QUEUE = f'edx.{QUEUE_VARIANT}core.high_mem'

CELERY_DEFAULT_QUEUE = DEFAULT_PRIORITY_QUEUE
CELERY_DEFAULT_ROUTING_KEY = DEFAULT_PRIORITY_QUEUE

CELERY_QUEUES = {
    HIGH_PRIORITY_QUEUE: {},
    DEFAULT_PRIORITY_QUEUE: {},
    HIGH_MEM_QUEUE: {},
}

CELERY_ROUTES = "openedx.core.lib.celery.routers.route_task"
CELERYBEAT_SCHEDULE = {}  # For scheduling tasks, entries can be added to this dict

CELERY_QUEUE_HA_POLICY = 'all'

CELERY_CREATE_MISSING_QUEUES = True

# let logging work as configured:
CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_BROKER_VHOST = ''
CELERY_BROKER_USE_SSL = False
CELERY_EVENT_QUEUE_TTL = None

CELERY_BROKER_TRANSPORT = 'amqp'
CELERY_BROKER_HOSTNAME = 'localhost'
CELERY_BROKER_USER = 'celery'
CELERY_BROKER_PASSWORD = 'celery'

############################## HEARTBEAT ######################################

# Checks run in normal mode by the heartbeat djangoapp
HEARTBEAT_CHECKS = [
    'openedx.core.djangoapps.heartbeat.default_checks.check_modulestore',
    'openedx.core.djangoapps.heartbeat.default_checks.check_database',
]

# Other checks to run by default in "extended"/heavy mode
HEARTBEAT_EXTENDED_CHECKS = (
    'openedx.core.djangoapps.heartbeat.default_checks.check_celery',
)

HEARTBEAT_CELERY_TIMEOUT = 5
HEARTBEAT_CELERY_ROUTING_KEY = HIGH_PRIORITY_QUEUE

################################ Block Structures ###################################

# .. setting_name: BLOCK_STRUCTURES_SETTINGS
# .. setting_default: dict of settings
# .. setting_description: Stores all the settings used by block structures and block structure
#   related tasks. See BLOCK_STRUCTURES_SETTINGS[XXX] documentation for details of each setting.
#   For more information, check https://github.com/openedx/edx-platform/pull/13388.
BLOCK_STRUCTURES_SETTINGS = dict(
    # .. setting_name: BLOCK_STRUCTURES_SETTINGS['COURSE_PUBLISH_TASK_DELAY']
    # .. setting_default: 30
    # .. setting_description: Delay, in seconds, after a new edit of a course is published before
    #   updating the block structures cache. This is needed for a better chance at getting
    #   the latest changes when there are secondary reads in sharded mongoDB clusters.
    #   For more information, check https://github.com/openedx/edx-platform/pull/13388 and
    #   https://github.com/openedx/edx-platform/pull/14571.
    COURSE_PUBLISH_TASK_DELAY=30,

    # .. setting_name: BLOCK_STRUCTURES_SETTINGS['TASK_DEFAULT_RETRY_DELAY']
    # .. setting_default: 30
    # .. setting_description: Delay, in seconds, between retry attempts if a block structure task
    #   fails. For more information, check https://github.com/openedx/edx-platform/pull/13388 and
    #   https://github.com/openedx/edx-platform/pull/14571.
    TASK_DEFAULT_RETRY_DELAY=30,

    # .. setting_name: BLOCK_STRUCTURES_SETTINGS['TASK_MAX_RETRIES']
    # .. setting_default: 5
    # .. setting_description: Maximum number of retries per block structure task.
    #   If the maximum number of retries is exceeded, then you can attempt to either manually run
    #   the celery task, or wait for it to be triggered again.
    #   For more information, check https://github.com/openedx/edx-platform/pull/13388 and
    #   https://github.com/openedx/edx-platform/pull/14571.
    TASK_MAX_RETRIES=5,
)

################################ Bulk Email ###################################

# Suffix used to construct 'from' email address for bulk emails.
# A course-specific identifier is prepended.
BULK_EMAIL_DEFAULT_FROM_EMAIL = 'no-reply@example.com'

# Parameters for breaking down course enrollment into subtasks.
BULK_EMAIL_EMAILS_PER_TASK = 500

# Initial delay used for retrying tasks.  Additional retries use
# longer delays.  Value is in seconds.
BULK_EMAIL_DEFAULT_RETRY_DELAY = 30

# Maximum number of retries per task for errors that are not related
# to throttling.
BULK_EMAIL_MAX_RETRIES = 5

# Maximum number of retries per task for errors that are related to
# throttling.  If this is not set, then there is no cap on such retries.
BULK_EMAIL_INFINITE_RETRY_CAP = 1000

# We want Bulk Email running on the high-priority queue, so we define the
# routing key that points to it.  At the moment, the name is the same.
BULK_EMAIL_ROUTING_KEY = HIGH_PRIORITY_QUEUE

# We also define a queue for smaller jobs so that large courses don't block
# smaller emails (see BULK_EMAIL_JOB_SIZE_THRESHOLD setting)
BULK_EMAIL_ROUTING_KEY_SMALL_JOBS = 'edx.lms.core.default'

# For emails with fewer than these number of recipients, send them through
# a different queue to avoid large courses blocking emails that are meant to be
# sent to self and staff
BULK_EMAIL_JOB_SIZE_THRESHOLD = 100

# Flag to indicate if individual email addresses should be logged as they are sent
# a bulk email message.
BULK_EMAIL_LOG_SENT_EMAILS = False

# Delay in seconds to sleep between individual mail messages being sent,
# when a bulk email task is retried for rate-related reasons.  Choose this
# value depending on the number of workers that might be sending email in
# parallel, and what the SES rate is.
BULK_EMAIL_RETRY_DELAY_BETWEEN_SENDS = 0.02

############################# Email Opt In ####################################

# Minimum age for organization-wide email opt in
EMAIL_OPTIN_MINIMUM_AGE = PARENTAL_CONSENT_AGE_LIMIT

############################## Video ##########################################

YOUTUBE = {
    # YouTube JavaScript API
    'API': 'https://www.youtube.com/iframe_api',

    'TEST_TIMEOUT': 1500,

    # URL to get YouTube metadata
    'METADATA_URL': 'https://www.googleapis.com/youtube/v3/videos/',

    # Web page mechanism for scraping transcript information from youtube video pages
    'TRANSCRIPTS': {
        'CAPTION_TRACKS_REGEX': r"captionTracks\"\:\[(?P<caption_tracks>[^\]]+)",
        'YOUTUBE_URL_BASE': 'https://www.youtube.com/watch?v=',
        'ALLOWED_LANGUAGE_CODES': ["en", "en-US", "en-GB"],
    },

    'IMAGE_API': 'http://img.youtube.com/vi/{youtube_id}/0.jpg',  # /maxresdefault.jpg for 1920*1080
}
YOUTUBE_API_KEY = 'PUT_YOUR_API_KEY_HERE'

################################### APPS ######################################

# The order of INSTALLED_APPS is important, when adding new apps here remember to check that you are not creating new
# RemovedInDjango19Warnings in the test logs.
#
# If you want to add a new djangoapp that isn't suitable for everyone, you have some options:
# - Add it to OPTIONAL_APPS below (registered if importable)
# - Add it to the ADDL_INSTALLED_APPS configuration variable (acts like EXTRA_APPS in other IDAs)
# - Make it a plugin (which are auto-registered) and add it to the EDXAPP_PRIVATE_REQUIREMENTS configuration variable
#   (See https://github.com/openedx/edx-django-utils/tree/master/edx_django_utils/plugins)
INSTALLED_APPS = [
    # Standard ones that are always installed...
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',

    # Tweaked version of django.contrib.staticfiles
    'openedx.core.djangoapps.staticfiles.apps.EdxPlatformStaticFilesConfig',

    'django_celery_results',

    # Common Initialization
    'openedx.core.djangoapps.common_initialization.apps.CommonInitializationConfig',

    # LMS-specific Initialization
    'lms.djangoapps.lms_initialization.apps.LMSInitializationConfig',

    # Common views
    'openedx.core.djangoapps.common_views',

    # History tables
    'simple_history',

    # Database-backed configuration
    'config_models',
    'openedx.core.djangoapps.config_model_utils',
    'waffle',

    # Monitor the status of services
    'openedx.core.djangoapps.service_status',

    # Display status message to students
    'common.djangoapps.status',

    # For asset pipelining
    'common.djangoapps.edxmako.apps.EdxMakoConfig',
    'pipeline',
    'common.djangoapps.static_replace',
    'webpack_loader',

    # For user interface plugins
    'web_fragments',
    'openedx.core.djangoapps.plugin_api',

    # For content serving
    'openedx.core.djangoapps.contentserver',

    # Site configuration for theming and behavioral modification
    'openedx.core.djangoapps.site_configuration',

    # Video block configs (This will be moved to Video once it becomes an XBlock)
    'openedx.core.djangoapps.video_config',

    # edX Video Pipeline integration
    'openedx.core.djangoapps.video_pipeline',

    # Our courseware
    'lms.djangoapps.courseware',
    'lms.djangoapps.coursewarehistoryextended',
    'common.djangoapps.student.apps.StudentConfig',
    'common.djangoapps.split_modulestore_django.apps.SplitModulestoreDjangoBackendAppConfig',

    'lms.djangoapps.static_template_view',
    'lms.djangoapps.staticbook',
    'common.djangoapps.track',
    'eventtracking.django.apps.EventTrackingConfig',
    'common.djangoapps.util',
    'lms.djangoapps.certificates.apps.CertificatesConfig',
    'lms.djangoapps.instructor_task',
    'openedx.core.djangoapps.course_groups',
    'lms.djangoapps.bulk_email',
    'lms.djangoapps.branding',

    # Course home api
    'lms.djangoapps.course_home_api',

    # User tours
    'lms.djangoapps.user_tours',

    # New (Learning-Core-based) XBlock runtime
    'openedx.core.djangoapps.xblock.apps.LmsXBlockAppConfig',

    # Student support tools
    'lms.djangoapps.support',

    # django-oauth-toolkit
    'oauth2_provider',
    'openedx.core.djangoapps.oauth_dispatch.apps.OAuthDispatchAppConfig',

    'common.djangoapps.third_party_auth',

    # System Wide Roles
    'openedx.core.djangoapps.system_wide_roles',

    'openedx.core.djangoapps.auth_exchange',

    # For the wiki
    'wiki',  # The new django-wiki from benjaoming
    'django_notify',
    'lms.djangoapps.course_wiki',  # Our customizations
    'mptt',
    'sekizai',
    #'wiki.plugins.attachments',
    'wiki.plugins.links',
    # Notifications were enabled, but only 11 people used it in three years. It
    # got tangled up during the Django 1.8 migration, so we are disabling it.
    # See TNL-3783 for details.
    #'wiki.plugins.notifications',
    'lms.djangoapps.course_wiki.plugins.markdownedx',

    # For testing
    'django.contrib.admin',  # only used in DEBUG mode
    'lms.djangoapps.debug',
    'openedx.core.djangoapps.util.apps.UtilConfig',

    # Discussion forums
    'openedx.core.djangoapps.django_comment_common',

    # Notes
    'lms.djangoapps.edxnotes',

    # Django Rest Framework
    'rest_framework',

    # REST framework JWT Auth
    'rest_framework_jwt',

    # User API
    'openedx.core.djangoapps.user_api',

    # Different Course Modes
    'common.djangoapps.course_modes.apps.CourseModesConfig',

    # Enrollment API
    'openedx.core.djangoapps.enrollments.apps.EnrollmentsConfig',

    # Entitlement API
    'common.djangoapps.entitlements.apps.EntitlementsConfig',

    # Bulk Enrollment API
    'lms.djangoapps.bulk_enroll',

    # Student Identity Verification
    'lms.djangoapps.verify_student.apps.VerifyStudentConfig',

    # Dark-launching languages
    'openedx.core.djangoapps.dark_lang',

    # RSS Proxy
    'lms.djangoapps.rss_proxy',

    # Country embargo support
    'openedx.core.djangoapps.embargo',

    # Course action state
    'common.djangoapps.course_action_state',

    # Country list
    'django_countries',

    # edX Mobile API
    'lms.djangoapps.mobile_api.apps.MobileApiConfig',
    'social_django',

    # Surveys
    'lms.djangoapps.survey.apps.SurveyConfig',

    'lms.djangoapps.lms_xblock.apps.LMSXBlockConfig',

    # Course data caching
    'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig',
    'openedx.core.djangoapps.content.block_structure.apps.BlockStructureConfig',
    'lms.djangoapps.course_blocks',

    # Mailchimp Syncing
    'lms.djangoapps.mailing',

    # CORS and cross-domain CSRF
    'corsheaders',
    'openedx.core.djangoapps.cors_csrf',

    'lms.djangoapps.commerce.apps.CommerceConfig',

    # Credit courses
    'openedx.core.djangoapps.credit.apps.CreditConfig',

    # Course teams
    'lms.djangoapps.teams',

    'common.djangoapps.xblock_django',

    # programs support
    'openedx.core.djangoapps.programs.apps.ProgramsConfig',

    # Catalog integration
    'openedx.core.djangoapps.catalog',

    'sorl.thumbnail',

    # edx-milestones service
    'milestones',

    # Gating of course content
    'lms.djangoapps.gating.apps.GatingConfig',

    # Static i18n support
    'statici18n',

    # API access administration
    'openedx.core.djangoapps.api_admin',

    # Verified Track Content Cohorting (Beta feature that will hopefully be removed)
    'openedx.core.djangoapps.verified_track_content',

    # Learner's dashboard
    'lms.djangoapps.learner_dashboard',

    # Needed whether or not enabled, due to migrations
    'lms.djangoapps.badges.apps.BadgesConfig',

    # Enables default site and redirects
    'django_sites_extensions',

    # Email marketing integration
    'lms.djangoapps.email_marketing.apps.EmailMarketingConfig',

    # additional release utilities to ease automation
    'release_util',

    # rule-based authorization
    'rules.apps.AutodiscoverRulesConfig',
    'bridgekeeper',

    # management of user-triggered async tasks (course import/export, etc.)
    'user_tasks',

    # Customized celery tasks, including persisting failed tasks so they can
    # be retried
    'celery_utils',

    # Ability to detect and special-case crawler behavior
    'openedx.core.djangoapps.crawlers',

    # Unusual migrations
    'common.djangoapps.database_fixups',

    'openedx.core.djangoapps.waffle_utils',

    # Course Goals
    'lms.djangoapps.course_goals.apps.CourseGoalsConfig',

    # Tagging
    'openedx_tagging.core.tagging.apps.TaggingConfig',
    'openedx.core.djangoapps.content_tagging',

    # Features
    'openedx.features.calendar_sync',
    'openedx.features.course_bookmarks',
    'openedx.features.course_experience',
    'openedx.features.enterprise_support.apps.EnterpriseSupportConfig',
    'openedx.features.learner_profile',
    'openedx.features.course_duration_limits',
    'openedx.features.content_type_gating',
    'openedx.features.discounts',
    'openedx.features.effort_estimation',
    'openedx.features.name_affirmation_api.apps.NameAffirmationApiConfig',

    'lms.djangoapps.experiments',

    # DRF filters
    'django_filters',

    # API Documentation
    'drf_yasg',

    # edx-drf-extensions
    'csrf.apps.CsrfAppConfig',  # Enables frontend apps to retrieve CSRF tokens.
    'xss_utils',

    # so sample_task is available to celery workers
    'openedx.core.djangoapps.heartbeat',

    # signal handlers to capture course dates into edx-when
    'openedx.core.djangoapps.course_date_signals',

    # Management of external user ids
    'openedx.core.djangoapps.external_user_ids',

    # Management of per-user schedules
    'openedx.core.djangoapps.schedules',

    # Learning Sequence Navigation
    'openedx.core.djangoapps.content.learning_sequences.apps.LearningSequencesConfig',

    # Database-backed Organizations App (http://github.com/openedx/edx-organizations)
    'organizations',

    # Bulk User Retirement
    'lms.djangoapps.bulk_user_retirement',

    # Agreements
    'openedx.core.djangoapps.agreements',

    # Survey reports
    'openedx.features.survey_report',

    # User and group management via edx-django-utils
    'edx_django_utils.user',

    # Content Library LTI 1.3 Support.
    'pylti1p3.contrib.django.lti1p3_tool_config',

    # For edx ace template tags
    'edx_ace',

    # MFE API
    'lms.djangoapps.mfe_config_api',

    # Notifications
    'openedx.core.djangoapps.notifications',

    'openedx_events',

    # Learning Core Apps, used by v2 content libraries (content_libraries app)
    "openedx_learning.apps.authoring.components",
    "openedx_learning.apps.authoring.contents",
    "openedx_learning.apps.authoring.publishing",
]


######################### CSRF #########################################

# Forwards-compatibility with Django 1.7
CSRF_COOKIE_AGE = 60 * 60 * 24 * 7 * 52
# It is highly recommended that you override this in any environment accessed by
# end users
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = []
CSRF_TRUSTED_ORIGINS_WITH_SCHEME = []
CROSS_DOMAIN_CSRF_COOKIE_DOMAIN = ''
CROSS_DOMAIN_CSRF_COOKIE_NAME = ''

######################### Django Rest Framework ########################

REST_FRAMEWORK = {
    # These default classes add observability around endpoints using defaults, and should
    # not be used anywhere else.
    # Notes on Order:
    # 1. `JwtAuthentication` does not check `is_active`, so email validation does not affect it. However,
    #    `SessionAuthentication` does. These work differently, and order changes in what way, which really stinks. See
    #    https://github.com/openedx/public-engineering/issues/165 for details.
    # 2. `JwtAuthentication` may also update the database based on contents. Since the LMS creates these JWTs, this
    #    shouldn't have any affect at this time. But it could, when and if another service started creating the JWTs.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'openedx.core.djangolib.default_auth_classes.DefaultJwtAuthentication',
        'openedx.core.djangolib.default_auth_classes.DefaultSessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'edx_rest_framework_extensions.paginators.DefaultPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'openedx.core.lib.request_utils.ignored_error_exception_handler',
    'PAGE_SIZE': 10,
    'URL_FORMAT_OVERRIDE': None,
    'DEFAULT_THROTTLE_RATES': {
        'user': '60/minute',
        'service_user': '800/minute',
        'registration_validation': '30/minute',
        'high_service_user': '2000/minute',
    },
}

# .. setting_name: REGISTRATION_VALIDATION_RATELIMIT
# .. setting_default: 30/7d
# .. setting_description: Whenever a user tries to register on edx, the data entered during registration
#    is validated via RegistrationValidationView.
#    It's POST endpoint is rate-limited up to 30 requests per IP Address in a week by default.
#    It was introduced because an attacker can guess or brute force a series of names to enumerate valid users.
# .. setting_tickets: https://github.com/openedx/edx-platform/pull/24664
REGISTRATION_VALIDATION_RATELIMIT = '30/7d'

# .. setting_name: REGISTRATION_RATELIMIT
# .. setting_default: 60/7d
# .. setting_description: New users are registered on edx via RegistrationView.
#    It's POST end-point is rate-limited up to 60 requests per IP Address in a week by default.
#    Purpose of this setting is to restrict an attacker from registering numerous fake accounts.
# .. setting_tickets: https://github.com/openedx/edx-platform/pull/27060
REGISTRATION_RATELIMIT = '60/7d'

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'openedx.core.apidocs.api_info',
    'DEEP_LINKING': True,
}

# How long to cache OpenAPI schemas and UI, in seconds.
OPENAPI_CACHE_TIMEOUT = 0

######################### MARKETING SITE ###############################
EDXMKTG_LOGGED_IN_COOKIE_NAME = 'edxloggedin'
EDXMKTG_USER_INFO_COOKIE_NAME = 'edx-user-info'
EDXMKTG_USER_INFO_COOKIE_VERSION = 1

MKTG_URLS = {}
MKTG_URL_OVERRIDES = {}
MKTG_URL_LINK_MAP = {
    'ABOUT': 'about',
    'CONTACT': 'contact',
    'FAQ': 'help',
    'COURSES': 'courses',
    'ROOT': 'root',
    'TOS': 'tos',
    'HONOR': 'honor',  # If your site does not have an honor code, simply delete this line.
    'TOS_AND_HONOR': 'edx-terms-service',
    'PRIVACY': 'privacy',
    'PRESS': 'press',
    'BLOG': 'blog',
    'DONATE': 'donate',
    'SITEMAP.XML': 'sitemap_xml',

    # Verified Certificates
    'WHAT_IS_VERIFIED_CERT': 'verified-certificate',
}

STATIC_TEMPLATE_VIEW_DEFAULT_FILE_EXTENSION = 'html'

SUPPORT_SITE_LINK = ''
ID_VERIFICATION_SUPPORT_LINK = ''
PASSWORD_RESET_SUPPORT_LINK = ''
ACTIVATION_EMAIL_SUPPORT_LINK = ''
LOGIN_ISSUE_SUPPORT_LINK = ''

# .. setting_name: SECURITY_PAGE_URL
# .. setting_default: None
# .. setting_description: A link to the site's security disclosure/reporting policy,
#   to display in the site footer. This will only appear for sites using themes that
#   use the links produced by ``lms.djangoapps.branding.api.get_footer``.
SECURITY_PAGE_URL = None

# Days before the expired date that we warn the user
ENTITLEMENT_EXPIRED_ALERT_PERIOD = 90

############################# SOCIAL MEDIA SHARING #############################
# Social Media Sharing on Student Dashboard
SOCIAL_SHARING_SETTINGS = {
    # Note: Ensure 'CUSTOM_COURSE_URLS' has a matching value in cms/envs/common.py
    'CUSTOM_COURSE_URLS': False,
    'DASHBOARD_FACEBOOK': False,
    'FACEBOOK_BRAND': None,
    'CERTIFICATE_FACEBOOK': False,
    'CERTIFICATE_FACEBOOK_TEXT': None,
    'CERTIFICATE_TWITTER': False,
    'CERTIFICATE_TWITTER_TEXT': None,
    'DASHBOARD_TWITTER': False,
    'DASHBOARD_TWITTER_TEXT': None,
    'TWITTER_BRAND': None
}

################# Social Media Footer Links #######################
# The names list controls the order of social media
# links in the footer.
SOCIAL_MEDIA_FOOTER_NAMES = [
    "facebook",
    "twitter",
    # "youtube", see PROD-816 for more details
    "linkedin",
    "instagram",
    "reddit",
]

# The footer URLs dictionary maps social footer names
# to URLs defined in configuration.
SOCIAL_MEDIA_FOOTER_ACE_URLS = {
    'reddit': 'http://www.reddit.com/r/edx',
    'twitter': 'https://twitter.com/edXOnline',
    'linkedin': 'http://www.linkedin.com/company/edx',
    'facebook': 'http://www.facebook.com/EdxOnline',
}

# The mobile store URLs dictionary maps mobile store names
# to URLs defined in configuration.
MOBILE_STORE_ACE_URLS = {
    'google': 'https://play.google.com/store/apps/details?id=org.edx.mobile',
    'apple': 'https://itunes.apple.com/us/app/edx/id945480667?mt=8',
}

# The social media logo urls dictionary maps social media names
# to the respective icons
SOCIAL_MEDIA_LOGO_URLS = {
    'reddit': 'http://email-media.s3.amazonaws.com/edX/2021/social_5_reddit.png',
    'twitter': 'http://email-media.s3.amazonaws.com/edX/2021/social_2_twitter.png',
    'linkedin': 'http://email-media.s3.amazonaws.com/edX/2021/social_3_linkedin.png',
    'facebook': 'http://email-media.s3.amazonaws.com/edX/2021/social_1_fb.png',
}

# The mobile store logo urls dictionary maps mobile store names
# to the respective icons
MOBILE_STORE_LOGO_URLS = {
    'google': 'http://email-media.s3.amazonaws.com/edX/2021/store_google_253x78.jpg',
    'apple': 'http://email-media.s3.amazonaws.com/edX/2021/store_apple_229x78.jpg',
}


# The display dictionary defines the title
# and icon class for each social media link.
SOCIAL_MEDIA_FOOTER_DISPLAY = {
    "facebook": {
        # Translators: This is the website name of www.facebook.com.  Please
        # translate this the way that Facebook advertises in your language.
        "title": _("Facebook"),
        "icon": "fa-facebook-square",
        "action": _("Like {platform_name} on Facebook")
    },
    "twitter": {
        # Translators: This is the website name of www.twitter.com.  Please
        # translate this the way that Twitter advertises in your language.
        "title": _("Twitter"),
        "icon": "fa-twitter-square",
        "action": _("Follow {platform_name} on Twitter")
    },
    "linkedin": {
        # Translators: This is the website name of www.linkedin.com.  Please
        # translate this the way that LinkedIn advertises in your language.
        "title": _("LinkedIn"),
        "icon": "fa-linkedin-square",
        "action": _("Follow {platform_name} on LinkedIn")
    },
    "instagram": {
        # Translators: This is the website name of www.instagram.com.  Please
        # translate this the way that Instagram advertises in your language.
        "title": _("Instagram"),
        "icon": "fa-instagram",
        "action": _("Follow {platform_name} on Instagram")
    },
    "tumblr": {
        # Translators: This is the website name of www.tumblr.com.  Please
        # translate this the way that Tumblr advertises in your language.
        "title": _("Tumblr"),
        "icon": "fa-tumblr"
    },
    "meetup": {
        # Translators: This is the website name of www.meetup.com.  Please
        # translate this the way that MeetUp advertises in your language.
        "title": _("Meetup"),
        "icon": "fa-calendar"
    },
    "reddit": {
        # Translators: This is the website name of www.reddit.com.  Please
        # translate this the way that Reddit advertises in your language.
        "title": _("Reddit"),
        "icon": "fa-reddit-square",
        "action": _("Subscribe to the {platform_name} subreddit"),
    },
    "vk": {
        # Translators: This is the website name of https://vk.com.  Please
        # translate this the way that VK advertises in your language.
        "title": _("VK"),
        "icon": "fa-vk"
    },
    "weibo": {
        # Translators: This is the website name of http://www.weibo.com.  Please
        # translate this the way that Weibo advertises in your language.
        "title": _("Weibo"),
        "icon": "fa-weibo"
    },
    "youtube": {
        # Translators: This is the website name of www.youtube.com.  Please
        # translate this the way that YouTube advertises in your language.
        "title": _("Youtube"),
        "icon": "fa-youtube-square",
        "action": _("Subscribe to the {platform_name} YouTube channel")
    }
}

#################SOCAIL AUTH OAUTH######################
SOCIAL_AUTH_OAUTH_SECRETS = {}

################# Student Verification #################
VERIFY_STUDENT = {
    "DAYS_GOOD_FOR": 365,  # How many days is a verficiation good for?
    # The variable represents the window within which a verification is considered to be "expiring soon."
    "EXPIRING_SOON_WINDOW": 28,
}

################# Student Verification Expiry Email #################
VERIFICATION_EXPIRY_EMAIL = {
    "RESEND_DAYS": 15,
    "DAYS_RANGE": 1,
    "DEFAULT_EMAILS": 2,
}

DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH = "verify_student_disable_account_activation_requirement"

################ Enable credit eligibility feature ####################
ENABLE_CREDIT_ELIGIBILITY = True
# .. toggle_name: FEATURES['ENABLE_CREDIT_ELIGIBILITY']
# .. toggle_implementation: DjangoSetting
# .. toggle_default: True
# .. toggle_description: When enabled, it is possible to define a credit eligibility criteria in the CMS. A "Credit
#   Eligibility" section then appears for those courses in the LMS.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2015-06-17
# .. toggle_tickets: https://github.com/openedx/edx-platform/pull/8550
FEATURES['ENABLE_CREDIT_ELIGIBILITY'] = ENABLE_CREDIT_ELIGIBILITY

############# Cross-domain requests #################

if FEATURES.get('ENABLE_CORS_HEADERS'):
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = ()
    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ALLOW_INSECURE = False

# Set CORS_ALLOW_HEADERS regardless of whether we've enabled ENABLE_CORS_HEADERS
# because that decision might happen in a later config file. (The headers to
# allow is an application logic, and not site policy.)
CORS_ALLOW_HEADERS = corsheaders_default_headers + (
    'use-jwt-cookie',
)

# Default cache expiration for the cross-domain proxy HTML page.
# This is a static page that can be iframed into an external page
# to simulate cross-domain requests.
XDOMAIN_PROXY_CACHE_TIMEOUT = 60 * 15

# .. setting_name: LOGIN_REDIRECT_WHITELIST
# .. setting_default: empty list ([])
# .. setting_description: While logout, if logout request has a redirect-url as query strings,
#   then the redirect-url is validated through LOGIN_REDIRECT_WHITELIST.
LOGIN_REDIRECT_WHITELIST = []

###################### Registration ##################################

# .. setting_name: REGISTRATION_EXTRA_FIELDS
# .. setting_default: {'confirm_email': 'hidden', 'level_of_education': 'optional', 'gender': 'optional',
#   'year_of_birth': 'optional', 'mailing_address': 'optional', 'goals': 'optional', 'honor_code': 'required',
#   'terms_of_service': 'hidden', 'city': 'hidden', 'country': 'hidden'}
# .. setting_description: The signup form may contain extra fields that are presented to every user. For every field, we
#   can specifiy whether it should be "required": to display the field, and make it mandatory; "optional": to display
#   the optional field as part of a toggled input field list; "optional-exposed": to display the optional fields among
#   the required fields, and make it non-mandatory; "hidden": to not display the field.
#   When the terms of service are not visible and agreement to the honor code is required (the default), the signup page
#   includes a paragraph that links to the honor code page (defined my MKTG_URLS["HONOR"]). This page might not be
#   available for all Open edX platforms. In such cases, the "honor_code" registration field should be "hidden".
REGISTRATION_EXTRA_FIELDS = {
    'confirm_email': 'hidden',
    'level_of_education': 'optional',
    'gender': 'optional',
    'year_of_birth': 'optional',
    'mailing_address': 'optional',
    'goals': 'optional',
    'honor_code': 'required',
    'terms_of_service': 'hidden',
    'city': 'hidden',
    'country': 'hidden',
}

REGISTRATION_FIELD_ORDER = [
    "name",
    "first_name",
    "last_name",
    "username",
    "email",
    "confirm_email",
    "password",
    "city",
    "state",
    "country",
    "year_of_birth",
    "level_of_education",
    "gender",
    "specialty",
    "profession",
    "company",
    "title",
    "mailing_address",
    "goals",
    "honor_code",
    "terms_of_service",
]

# Optional setting to restrict registration / account creation to only emails
# that match a regex in this list. Set to None to allow any email (default).
REGISTRATION_EMAIL_PATTERNS_ALLOWED = None

# String length for the configurable part of the auto-generated username
AUTO_GENERATED_USERNAME_RANDOM_STRING_LENGTH = 4

########################## CERTIFICATE NAME ########################
CERT_NAME_SHORT = "Certificate"
CERT_NAME_LONG = "Certificate of Achievement"

###################### Grade Downloads ######################
# These keys are used for all of our asynchronous downloadable files, including
# the ones that contain information other than grades.
GRADES_DOWNLOAD_ROUTING_KEY = HIGH_MEM_QUEUE

POLICY_CHANGE_GRADES_ROUTING_KEY = 'edx.lms.core.default'

SINGLE_LEARNER_COURSE_REGRADE_ROUTING_KEY = 'edx.lms.core.default'

RECALCULATE_GRADES_ROUTING_KEY = 'edx.lms.core.default'

SOFTWARE_SECURE_VERIFICATION_ROUTING_KEY = 'edx.lms.core.default'

GRADES_DOWNLOAD = {
    'STORAGE_CLASS': 'django.core.files.storage.FileSystemStorage',
    'STORAGE_KWARGS': {
        'location': '/tmp/edx-s3/grades',
    },
    'STORAGE_TYPE': None,
    'BUCKET': None,
    'ROOT_PATH': None,
}

FINANCIAL_REPORTS = {
    'STORAGE_TYPE': 'localfs',
    'BUCKET': None,
    'ROOT_PATH': 'sandbox',
}

#### Grading policy change-related settings #####
# Rate limit for regrading tasks that a grading policy change can kick off
POLICY_CHANGE_TASK_RATE_LIMIT = '900/h'

#### PASSWORD POLICY SETTINGS #####
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "common.djangoapps.util.password_policy_validators.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8
        }
    },
    {
        "NAME": "common.djangoapps.util.password_policy_validators.MaximumLengthValidator",
        "OPTIONS": {
            "max_length": 75
        }
    },
]

PASSWORD_POLICY_COMPLIANCE_ROLLOUT_CONFIG = {
    'ENFORCE_COMPLIANCE_ON_LOGIN': False
}

############################ ORA 2 ############################################
ORA_WORKFLOW_UPDATE_ROUTING_KEY = "edx.lms.core.ora_workflow_update"

# By default, don't use a file prefix
ORA2_FILE_PREFIX = None

# Default File Upload Storage bucket and prefix. Used by the FileUpload Service.
FILE_UPLOAD_STORAGE_BUCKET_NAME = 'SET-ME-PLEASE (ex. bucket-name)'
FILE_UPLOAD_STORAGE_PREFIX = 'submissions_attachments'

##### ACCOUNT LOCKOUT DEFAULT PARAMETERS #####
# .. setting_name: MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED
# .. setting_default: 6
# .. setting_description: Specifies the maximum failed login attempts allowed to users. Once the user reaches this
#   failure threshold then the account will be locked for a configurable amount of seconds (30 minutes) which will
#   prevent additional login attempts until this time period has passed. This setting is related with
#   MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS and only used when ENABLE_MAX_FAILED_LOGIN_ATTEMPTS is enabled.
MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED = 6

# .. setting_name: MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS
# .. setting_default: 30 * 60
# .. setting_description: Specifies the lockout period in seconds for consecutive failed login attempts. Once the user
#   reaches the threshold of the login failure, then the account will be locked for the given amount of seconds
#   (30 minutes) which will prevent additional login attempts until this time period has passed. This setting is
#   related with MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED and only used when ENABLE_MAX_FAILED_LOGIN_ATTEMPTS is enabled.
MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS = 30 * 60


##### LMS DEADLINE DISPLAY TIME_ZONE #######
TIME_ZONE_DISPLAYED_FOR_DEADLINES = 'UTC'


########################## VIDEO IMAGE STORAGE ############################

VIDEO_IMAGE_SETTINGS = dict(
    VIDEO_IMAGE_MAX_BYTES=2 * 1024 * 1024,    # 2 MB
    VIDEO_IMAGE_MIN_BYTES=2 * 1024,       # 2 KB
    # Backend storage
    # STORAGE_CLASS='storages.backends.s3boto3.S3Boto3Storage',
    # STORAGE_KWARGS=dict(bucket='video-image-bucket'),
    STORAGE_KWARGS=dict(
        location=MEDIA_ROOT,
    ),
    DIRECTORY_PREFIX='video-images/',
    BASE_URL=MEDIA_URL,

)

VIDEO_IMAGE_MAX_AGE = 31536000

########################## VIDEO TRANSCRIPTS STORAGE ############################

VIDEO_TRANSCRIPTS_SETTINGS = dict(
    VIDEO_TRANSCRIPTS_MAX_BYTES=3 * 1024 * 1024,    # 3 MB
    # Backend storage
    # STORAGE_CLASS='storages.backends.s3boto3.S3Boto3Storage',
    # STORAGE_KWARGS=dict(bucket='video-transcripts-bucket'),
    STORAGE_KWARGS=dict(
        location=MEDIA_ROOT,
    ),
    DIRECTORY_PREFIX='video-transcripts/',
    BASE_URL=MEDIA_URL,
)

VIDEO_TRANSCRIPTS_MAX_AGE = 31536000

# Source:
# http://loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt according to http://en.wikipedia.org/wiki/ISO_639-1
# Note that this is used as the set of choices to the `code` field of the
# `LanguageProficiency` model.
ALL_LANGUAGES = [
    ["aa", "Afar"],
    ["ab", "Abkhazian"],
    ["af", "Afrikaans"],
    ["ak", "Akan"],
    ["sq", "Albanian"],
    ["am", "Amharic"],
    ["ar", "Arabic"],
    ["an", "Aragonese"],
    ["hy", "Armenian"],
    ["as", "Assamese"],
    ["av", "Avaric"],
    ["ae", "Avestan"],
    ["ay", "Aymara"],
    ["az", "Azerbaijani"],
    ["ba", "Bashkir"],
    ["bm", "Bambara"],
    ["eu", "Basque"],
    ["be", "Belarusian"],
    ["bn", "Bengali"],
    ["bh", "Bihari languages"],
    ["bi", "Bislama"],
    ["bs", "Bosnian"],
    ["br", "Breton"],
    ["bg", "Bulgarian"],
    ["my", "Burmese"],
    ["ca", "Catalan"],
    ["ch", "Chamorro"],
    ["ce", "Chechen"],
    ["zh", "Chinese"],
    ["zh_HANS", "Simplified Chinese"],
    ["zh_HANT", "Traditional Chinese"],
    ["cu", "Church Slavic"],
    ["cv", "Chuvash"],
    ["kw", "Cornish"],
    ["co", "Corsican"],
    ["cr", "Cree"],
    ["cs", "Czech"],
    ["da", "Danish"],
    ["dv", "Divehi"],
    ["nl", "Dutch"],
    ["dz", "Dzongkha"],
    ["en", "English"],
    ["eo", "Esperanto"],
    ["et", "Estonian"],
    ["ee", "Ewe"],
    ["fo", "Faroese"],
    ["fj", "Fijian"],
    ["fi", "Finnish"],
    ["fr", "French"],
    ["fy", "Western Frisian"],
    ["ff", "Fulah"],
    ["ka", "Georgian"],
    ["de", "German"],
    ["gd", "Gaelic"],
    ["ga", "Irish"],
    ["gl", "Galician"],
    ["gv", "Manx"],
    ["el", "Greek"],
    ["gn", "Guarani"],
    ["gu", "Gujarati"],
    ["ht", "Haitian"],
    ["ha", "Hausa"],
    ["he", "Hebrew"],
    ["hz", "Herero"],
    ["hi", "Hindi"],
    ["ho", "Hiri Motu"],
    ["hr", "Croatian"],
    ["hu", "Hungarian"],
    ["ig", "Igbo"],
    ["is", "Icelandic"],
    ["io", "Ido"],
    ["ii", "Sichuan Yi"],
    ["iu", "Inuktitut"],
    ["ie", "Interlingue"],
    ["ia", "Interlingua"],
    ["id", "Indonesian"],
    ["ik", "Inupiaq"],
    ["it", "Italian"],
    ["jv", "Javanese"],
    ["ja", "Japanese"],
    ["kl", "Kalaallisut"],
    ["kn", "Kannada"],
    ["ks", "Kashmiri"],
    ["kr", "Kanuri"],
    ["kk", "Kazakh"],
    ["km", "Central Khmer"],
    ["ki", "Kikuyu"],
    ["rw", "Kinyarwanda"],
    ["ky", "Kirghiz"],
    ["kv", "Komi"],
    ["kg", "Kongo"],
    ["ko", "Korean"],
    ["kj", "Kuanyama"],
    ["ku", "Kurdish"],
    ["lo", "Lao"],
    ["la", "Latin"],
    ["lv", "Latvian"],
    ["li", "Limburgan"],
    ["ln", "Lingala"],
    ["lt", "Lithuanian"],
    ["lb", "Luxembourgish"],
    ["lu", "Luba-Katanga"],
    ["lg", "Ganda"],
    ["mk", "Macedonian"],
    ["mh", "Marshallese"],
    ["ml", "Malayalam"],
    ["mi", "Maori"],
    ["mr", "Marathi"],
    ["ms", "Malay"],
    ["mg", "Malagasy"],
    ["mt", "Maltese"],
    ["mn", "Mongolian"],
    ["na", "Nauru"],
    ["nv", "Navajo"],
    ["nr", "Ndebele, South"],
    ["nd", "Ndebele, North"],
    ["ng", "Ndonga"],
    ["ne", "Nepali"],
    ["nn", "Norwegian Nynorsk"],
    ["nb", "Bokmål, Norwegian"],
    ["no", "Norwegian"],
    ["ny", "Chichewa"],
    ["oc", "Occitan"],
    ["oj", "Ojibwa"],
    ["or", "Oriya"],
    ["om", "Oromo"],
    ["os", "Ossetian"],
    ["pa", "Panjabi"],
    ["fa", "Persian"],
    ["pi", "Pali"],
    ["pl", "Polish"],
    ["pt", "Portuguese"],
    ["ps", "Pushto"],
    ["qu", "Quechua"],
    ["rm", "Romansh"],
    ["ro", "Romanian"],
    ["rn", "Rundi"],
    ["ru", "Russian"],
    ["sg", "Sango"],
    ["sa", "Sanskrit"],
    ["si", "Sinhala"],
    ["sk", "Slovak"],
    ["sl", "Slovenian"],
    ["se", "Northern Sami"],
    ["sm", "Samoan"],
    ["sn", "Shona"],
    ["sd", "Sindhi"],
    ["so", "Somali"],
    ["st", "Sotho, Southern"],
    ["es", "Spanish"],
    ["sc", "Sardinian"],
    ["sr", "Serbian"],
    ["ss", "Swati"],
    ["su", "Sundanese"],
    ["sw", "Swahili"],
    ["sv", "Swedish"],
    ["ty", "Tahitian"],
    ["ta", "Tamil"],
    ["tt", "Tatar"],
    ["te", "Telugu"],
    ["tg", "Tajik"],
    ["tl", "Tagalog"],
    ["th", "Thai"],
    ["bo", "Tibetan"],
    ["ti", "Tigrinya"],
    ["to", "Tonga (Tonga Islands)"],
    ["tn", "Tswana"],
    ["ts", "Tsonga"],
    ["tk", "Turkmen"],
    ["tr", "Turkish"],
    ["tw", "Twi"],
    ["ug", "Uighur"],
    ["uk", "Ukrainian"],
    ["ur", "Urdu"],
    ["uz", "Uzbek"],
    ["ve", "Venda"],
    ["vi", "Vietnamese"],
    ["vo", "Volapük"],
    ["cy", "Welsh"],
    ["wa", "Walloon"],
    ["wo", "Wolof"],
    ["xh", "Xhosa"],
    ["yi", "Yiddish"],
    ["yo", "Yoruba"],
    ["za", "Zhuang"],
    ["zu", "Zulu"]
]


### Apps only installed in some instances
# The order of INSTALLED_APPS matters, so this tuple is the app name and the item in INSTALLED_APPS
# that this app should be inserted *before*. A None here means it should be appended to the list.
OPTIONAL_APPS = [
    ('problem_builder', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),
    ('edx_sga', None),

    # edx-ora2
    ('submissions', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),
    ('openassessment', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),
    ('openassessment.assessment', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),
    ('openassessment.fileupload', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),
    ('openassessment.staffgrader', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),
    ('openassessment.workflow', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),
    ('openassessment.xblock', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),

    # edxval
    ('edxval', 'openedx.core.djangoapps.content.course_overviews.apps.CourseOverviewsConfig'),

    # Enterprise Apps (http://github.com/openedx/edx-enterprise)
    ('enterprise', None),
    ('consent', None),
    ('integrated_channels.integrated_channel', None),
    ('integrated_channels.degreed', None),
    ('integrated_channels.degreed2', None),
    ('integrated_channels.sap_success_factors', None),
    ('integrated_channels.cornerstone', None),
    ('integrated_channels.xapi', None),
    ('integrated_channels.blackboard', None),
    ('integrated_channels.canvas', None),
    ('integrated_channels.moodle', None),

    # Required by the Enterprise App
    ('django_object_actions', None),  # https://github.com/crccheck/django-object-actions
]

for app_name, insert_before in OPTIONAL_APPS:
    # First attempt to only find the module rather than actually importing it,
    # to avoid circular references - only try to import if it can't be found
    # by find_spec, which doesn't work with import hooks
    if importlib.util.find_spec(app_name) is None:
        try:
            __import__(app_name)
        except ImportError:
            continue

    try:
        INSTALLED_APPS.insert(INSTALLED_APPS.index(insert_before), app_name)
    except (IndexError, ValueError):
        INSTALLED_APPS.append(app_name)

### External auth usage -- prefixes for ENROLLMENT_DOMAIN
SHIBBOLETH_DOMAIN_PREFIX = 'shib:'

### Analytics API
ANALYTICS_API_KEY = ""
ANALYTICS_API_URL = "http://localhost:18100"
ANALYTICS_DASHBOARD_URL = 'http://localhost:18110/courses'
ANALYTICS_DASHBOARD_NAME = 'Your Platform Name Here Insights'

# REGISTRATION CODES DISPLAY INFORMATION SUBTITUTIONS IN THE INVOICE ATTACHMENT
INVOICE_CORP_ADDRESS = "Please place your corporate address\nin this configuration"
INVOICE_PAYMENT_INSTRUCTIONS = "This is where you can\nput directions on how people\nbuying registration codes"

# Country code overrides
# Used by django-countries
COUNTRIES_OVERRIDE = {
    # Taiwan is specifically not translated to avoid it being translated as "Taiwan (Province of China)"
    "TW": "Taiwan",
    'XK': _('Kosovo'),
}

# which access.py permission name to check in order to determine if a course is visible in
# the course catalog. We default this to the legacy permission 'see_exists'.
COURSE_CATALOG_VISIBILITY_PERMISSION = 'see_exists'

# which access.py permission name to check in order to determine if a course about page is
# visible. We default this to the legacy permission 'see_exists'.
COURSE_ABOUT_VISIBILITY_PERMISSION = 'see_exists'

DEFAULT_COURSE_VISIBILITY_IN_CATALOG = "both"

# .. toggle_name: DEFAULT_MOBILE_AVAILABLE
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: This specifies if the courses are available for mobile by default. To make any individual
#   course available for mobile one can set the value of Mobile Course Available to true in Advanced Settings from the
#   studio when this is False.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2021-01-26
# .. toggle_tickets: https://openedx.atlassian.net/browse/OSPR-1985
DEFAULT_MOBILE_AVAILABLE = False

# Enrollment API Cache Timeout
ENROLLMENT_COURSE_DETAILS_CACHE_TIMEOUT = 60

# These tabs are currently disabled
NOTES_DISABLED_TABS = ['course_structure', 'tags']

# Configuration used for generating PDF Receipts/Invoices
PDF_RECEIPT_TAX_ID = '00-0000000'
PDF_RECEIPT_FOOTER_TEXT = 'Enter your receipt footer text here.'
PDF_RECEIPT_DISCLAIMER_TEXT = 'ENTER YOUR RECEIPT DISCLAIMER TEXT HERE.'
PDF_RECEIPT_BILLING_ADDRESS = 'Enter your receipt billing address here.'
PDF_RECEIPT_TERMS_AND_CONDITIONS = 'Enter your receipt terms and conditions here.'
PDF_RECEIPT_TAX_ID_LABEL = 'fake Tax ID'
PDF_RECEIPT_LOGO_PATH = PROJECT_ROOT + '/static/images/openedx-logo-tag.png'
# Height of the Logo in mm
PDF_RECEIPT_LOGO_HEIGHT_MM = 12
PDF_RECEIPT_COBRAND_LOGO_PATH = PROJECT_ROOT + '/static/images/logo.png'
# Height of the Co-brand Logo in mm
PDF_RECEIPT_COBRAND_LOGO_HEIGHT_MM = 12

# Use None for the default search engine
SEARCH_ENGINE = None
# Use LMS specific search initializer
SEARCH_INITIALIZER = "lms.lib.courseware_search.lms_search_initializer.LmsSearchInitializer"
# Use the LMS specific result processor
SEARCH_RESULT_PROCESSOR = "lms.lib.courseware_search.lms_result_processor.LmsSearchResultProcessor"
# Use the LMS specific filter generator
SEARCH_FILTER_GENERATOR = "lms.lib.courseware_search.lms_filter_generator.LmsSearchFilterGenerator"
# Override to skip enrollment start date filtering in course search
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = False
# .. toggle_name: SEARCH_SKIP_INVITATION_ONLY_FILTERING
# .. toggle_implementation: DjangoSetting
# .. toggle_default: True
# .. toggle_description: If enabled, invitation-only courses will appear in search results.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2021-08-27
SEARCH_SKIP_INVITATION_ONLY_FILTERING = True
# .. toggle_name: SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING
# .. toggle_implementation: DjangoSetting
# .. toggle_default: True
# .. toggle_description: If enabled, courses with a catalog_visibility set to "none" will still
#    appear in search results.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2021-08-27
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = True

# The configuration visibility of account fields.
ACCOUNT_VISIBILITY_CONFIGURATION = {
    # Default visibility level for accounts without a specified value
    # The value is one of: 'all_users', 'private'
    "default_visibility": "all_users",

    # The list of account fields that are always public
    "public_fields": [
        'account_privacy',
        'profile_image',
        'username',
    ],
}

# The list of all fields that are shared with other users using the bulk 'all_users' privacy setting
ACCOUNT_VISIBILITY_CONFIGURATION["bulk_shareable_fields"] = (
    ACCOUNT_VISIBILITY_CONFIGURATION["public_fields"] + [
        'bio',
        'course_certificates',
        'country',
        'date_joined',
        'language_proficiencies',
        "level_of_education",
        'social_links',
        'time_zone',
    ]
)

# The list of all fields that can be shared selectively with other users using the 'custom' privacy setting
ACCOUNT_VISIBILITY_CONFIGURATION["custom_shareable_fields"] = (
    ACCOUNT_VISIBILITY_CONFIGURATION["bulk_shareable_fields"] + [
        "name",
    ]
)

# The list of account fields that are visible only to staff and users viewing their own profiles
ACCOUNT_VISIBILITY_CONFIGURATION["admin_fields"] = (
    ACCOUNT_VISIBILITY_CONFIGURATION["custom_shareable_fields"] + [
        "email",
        "id",
        "verified_name",
        "extended_profile",
        "gender",
        "state",
        "goals",
        "is_active",
        "last_login",
        "mailing_address",
        "requires_parental_consent",
        "secondary_email",
        "secondary_email_enabled",
        "year_of_birth",
        "phone_number",
        "activation_key",
        "pending_name_change",
    ]
)

# The current list of social platforms to be shown to the user.
#
# url_stub represents the host URL, it must end with a forward
# slash and represent the profile at https://www.[url_stub][username]
#
# The example will be used as a placeholder in the social link
# input field as well as in some messaging describing an example of a
# valid link.
SOCIAL_PLATFORMS = {
    'facebook': {
        'display_name': 'Facebook',
        'url_stub': 'facebook.com/',
        'example': 'https://www.facebook.com/username'
    },
    'twitter': {
        'display_name': 'Twitter',
        'url_stub': 'twitter.com/',
        'example': 'https://www.twitter.com/username'
    },
    'linkedin': {
        'display_name': 'LinkedIn',
        'url_stub': 'linkedin.com/in/',
        'example': 'www.linkedin.com/in/username'
    }
}

# Enable First Purchase Discount offer override
FIRST_PURCHASE_DISCOUNT_OVERRIDE_CODE = ''
FIRST_PURCHASE_DISCOUNT_OVERRIDE_PERCENTAGE = 15

# E-Commerce API Configuration
ECOMMERCE_PUBLIC_URL_ROOT = 'http://localhost:8002'
ECOMMERCE_API_URL = 'http://localhost:8002/api/v2'
ECOMMERCE_API_TIMEOUT = 5
ECOMMERCE_ORDERS_API_CACHE_TIMEOUT = 3600
ECOMMERCE_SERVICE_WORKER_USERNAME = 'ecommerce_worker'
ECOMMERCE_API_SIGNING_KEY = 'SET-ME-PLEASE'

# E-Commerce Commerce Coordinator Configuration
COMMERCE_COORDINATOR_URL_ROOT = 'http://localhost:8140'
COMMERCE_COORDINATOR_REFUND_PATH = '/lms/refund/'
COMMERCE_COORDINATOR_REFUND_SOURCE_SYSTEMS = ('SET-ME-PLEASE',)
COMMERCE_COORDINATOR_SERVICE_WORKER_USERNAME = 'commerce_coordinator_worker'
COORDINATOR_CHECKOUT_REDIRECT_PATH = '/lms/payment_page_redirect/'

# Exam Service
EXAMS_SERVICE_URL = 'http://localhost:18740/api/v1'

TOKEN_SIGNING = {
    'JWT_ISSUER': 'http://127.0.0.1:8740',
    'JWT_SIGNING_ALGORITHM': 'RS512',
    'JWT_SUPPORTED_VERSION': '1.2.0',
    'JWT_PUBLIC_SIGNING_JWK_SET': None,
}

COURSE_CATALOG_URL_ROOT = 'http://localhost:8008'
COURSE_CATALOG_API_URL = f'{COURSE_CATALOG_URL_ROOT}/api/v1'

CREDENTIALS_INTERNAL_SERVICE_URL = 'http://localhost:8005'
CREDENTIALS_PUBLIC_SERVICE_URL = 'http://localhost:8005'

COMMENTS_SERVICE_URL = 'http://localhost:18080'
COMMENTS_SERVICE_KEY = 'password'

# Reverification checkpoint name pattern
CHECKPOINT_PATTERN = r'(?P<checkpoint_name>[^/]+)'

# For the fields override feature
# If using FEATURES['INDIVIDUAL_DUE_DATES'], you should add
# 'lms.djangoapps.courseware.student_field_overrides.IndividualStudentOverrideProvider' to
# this setting.
FIELD_OVERRIDE_PROVIDERS = ()

# Modulestore-level field override providers. These field override providers don't
# require student context.
MODULESTORE_FIELD_OVERRIDE_PROVIDERS = ('openedx.features.content_type_gating.'
                                        'field_override.ContentTypeGatingFieldOverride',)

# PROFILE IMAGE CONFIG
# WARNING: Certain django storage backends do not support atomic
# file overwrites (including the default, OverwriteStorage) - instead
# there are separate calls to delete and then write a new file in the
# storage backend.  This introduces the risk of a race condition
# occurring when a user uploads a new profile image to replace an
# earlier one (the file will temporarily be deleted).
PROFILE_IMAGE_BACKEND = {
    'class': 'openedx.core.storage.OverwriteStorage',
    'options': {
        'location': os.path.join(MEDIA_ROOT, 'profile-images/'),
        'base_url': os.path.join(MEDIA_URL, 'profile-images/'),
    },
}
PROFILE_IMAGE_DEFAULT_FILENAME = 'images/profiles/default'
PROFILE_IMAGE_DEFAULT_FILE_EXTENSION = 'png'
# This key is used in generating unguessable URLs to users'
# profile images. Once it has been set, changing it will make the
# platform unaware of current image URLs.
PROFILE_IMAGE_HASH_SEED = 'placeholder_secret_key'
PROFILE_IMAGE_MAX_BYTES = 1024 * 1024
PROFILE_IMAGE_MIN_BYTES = 100
PROFILE_IMAGE_SIZES_MAP = {
    'full': 500,
    'large': 120,
    'medium': 50,
    'small': 30
}

# Sets the maximum number of courses listed on the homepage
# If set to None, all courses will be listed on the homepage
HOMEPAGE_COURSE_MAX = None

# .. setting_name: COURSE_MEMBER_API_ENROLLMENT_LIMIT
# .. setting_implementation: DjangoSetting
# .. setting_default: 1000
# .. setting_description: This limits the response size of the `get_course_members` API, throwing an exception
#    if the number of Enrolled users is greater than this number. This is needed to limit the dataset size
#    since the API does most of the calculation in Python to avoid expensive database queries.
# .. setting_use_cases: open_edx
# .. setting_creation_date: 2021-05-18
# .. setting_tickets: https://openedx.atlassian.net/browse/TNL-7330
COURSE_MEMBER_API_ENROLLMENT_LIMIT = 1000

################################ Settings for Credit Courses ################################
# Initial delay used for retrying tasks.
# Additional retries use longer delays.
# Value is in seconds.
CREDIT_TASK_DEFAULT_RETRY_DELAY = 30

# Maximum number of retries per task for errors that are not related
# to throttling.
CREDIT_TASK_MAX_RETRIES = 5

# Dummy secret key for dev/test
SECRET_KEY = 'dev key'

# Secret keys shared with credit providers.
# Used to digitally sign credit requests (us --> provider)
# and validate responses (provider --> us).
# Each key in the dictionary is a credit provider ID, and
# the value is the 32-character key.
CREDIT_PROVIDER_SECRET_KEYS = {}

# Maximum age in seconds of timestamps we will accept
# when a credit provider notifies us that a student has been approved
# or denied for credit.
CREDIT_PROVIDER_TIMESTAMP_EXPIRATION = 15 * 60

# The Help link to the FAQ page about the credit
CREDIT_HELP_LINK_URL = ""

# Default domain for the e-mail address associated with users who are created
# via the LTI Provider feature. Note that the generated e-mail addresses are
# not expected to be active; this setting simply allows administrators to
# route any messages intended for LTI users to a common domain.
LTI_USER_EMAIL_DOMAIN = 'lti.example.com'

# An aggregate score is one derived from multiple problems (such as the
# cumulative score for a vertical element containing many problems). Sending
# aggregate scores immediately introduces two issues: one is a race condition
# between the view method and the Celery task where the updated score may not
# yet be visible to the database if the view has not yet returned (and committed
# its transaction). The other is that the student is likely to receive a stream
# of notifications as the score is updated with every problem. Waiting a
# reasonable period of time allows the view transaction to end, and allows us to
# collapse multiple score updates into a single message.
# The time value is in seconds.
LTI_AGGREGATE_SCORE_PASSBACK_DELAY = 15 * 60

# Credit notifications settings
NOTIFICATION_EMAIL_CSS = "templates/credit_notifications/credit_notification.css"
NOTIFICATION_EMAIL_EDX_LOGO = "templates/credit_notifications/edx-logo-header.png"


################################ Settings for JWTs ################################

JWT_ISSUER = 'http://127.0.0.1:8000/oauth2'
DEFAULT_JWT_ISSUER = {
    'ISSUER': 'http://127.0.0.1:8000/oauth2',
    'AUDIENCE': 'change-me',
    'SECRET_KEY': 'SET-ME-PLEASE'
}
JWT_EXPIRATION = 30
JWT_PRIVATE_SIGNING_KEY = None

JWT_AUTH = {
    'JWT_VERIFY_EXPIRATION': True,

    'JWT_PAYLOAD_GET_USERNAME_HANDLER': lambda d: d.get('username'),
    'JWT_LEEWAY': 1,
    'JWT_DECODE_HANDLER': 'edx_rest_framework_extensions.auth.jwt.decoder.jwt_decode_handler',

    'JWT_AUTH_COOKIE': 'edx-jwt-cookie',

    # Number of seconds before JWTs expire
    'JWT_EXPIRATION': 30,
    'JWT_IN_COOKIE_EXPIRATION': 60 * 60,

    'JWT_LOGIN_CLIENT_ID': 'login-service-client-id',
    'JWT_LOGIN_SERVICE_USERNAME': 'login_service_user',

    'JWT_SUPPORTED_VERSION': '1.2.0',

    'JWT_ALGORITHM': 'HS256',
    'JWT_SECRET_KEY': SECRET_KEY,

    'JWT_SIGNING_ALGORITHM': 'RS512',
    'JWT_PRIVATE_SIGNING_JWK': None,
    'JWT_PUBLIC_SIGNING_JWK_SET': None,

    'JWT_ISSUER': 'http://127.0.0.1:8000/oauth2',
    'JWT_AUDIENCE': 'change-me',
    'JWT_ISSUERS': [
        {
            'ISSUER': 'http://127.0.0.1:8000/oauth2',
            'AUDIENCE': 'change-me',
            'SECRET_KEY': SECRET_KEY
        }
    ],
    'JWT_AUTH_COOKIE_HEADER_PAYLOAD': 'edx-jwt-cookie-header-payload',
    'JWT_AUTH_COOKIE_SIGNATURE': 'edx-jwt-cookie-signature',
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

EDX_DRF_EXTENSIONS = {
    # Set this value to an empty dict in order to prevent automatically updating
    # user data from values in (possibly stale) JWTs.
    'JWT_PAYLOAD_USER_ATTRIBUTE_MAPPING': {},
    # Allows JWT authentication to find the LMS user id for verification
    'VERIFY_LMS_USER_ID_PROPERTY_NAME': 'id',
}

################################ Settings for rss_proxy ################################

RSS_PROXY_CACHE_TIMEOUT = 3600  # The length of time we cache RSS retrieved from remote URLs in seconds

#### Custom Courses for EDX (CCX) configuration

# .. setting_name: CCX_MAX_STUDENTS_ALLOWED
# .. setting_default: 200
# .. setting_description: Maximum number of students allowed in a CCX (Custom Courses for edX), This is an arbitrary
#   hard limit, chosen so that a CCX does not compete with public MOOCs.
CCX_MAX_STUDENTS_ALLOWED = 200

# Financial assistance settings

# Maximum and minimum length of answers, in characters, for the
# financial assistance form
FINANCIAL_ASSISTANCE_MIN_LENGTH = 1250
FINANCIAL_ASSISTANCE_MAX_LENGTH = 2500

#### Registration form extension. ####
# Only used if combined login/registration is enabled.
# This can be used to add fields to the registration page.
# It must be a path to a valid form, in dot-separated syntax.
# IE: custom_form_app.forms.RegistrationExtensionForm
# Note: If you want to use a model to store the results of the form, you will
# need to add the model's app to the ADDL_INSTALLED_APPS array in your
# lms.yml file.

REGISTRATION_EXTENSION_FORM = None

# Identifier included in the User Agent from Open edX mobile apps.
MOBILE_APP_USER_AGENT_REGEXES = [
    r'edX/org.edx.mobile',
]

# set course limit for mobile search
MOBILE_SEARCH_COURSE_LIMIT = 100

# cache timeout in seconds for Mobile App Version Upgrade
APP_UPGRADE_CACHE_TIMEOUT = 3600

# Offset for courseware.StudentModuleHistoryExtended which is used to
# calculate the starting primary key for the underlying table.  This gap
# should be large enough that you do not generate more than N courseware.StudentModuleHistory
# records before you have deployed the app to write to coursewarehistoryextended.StudentModuleHistoryExtended
# if you want to avoid an overlap in ids while searching for history across the two tables.
STUDENTMODULEHISTORYEXTENDED_OFFSET = 10000

################################ Settings for Credentials Service ################################

CREDENTIALS_SERVICE_USERNAME = 'credentials_service_user'
CREDENTIALS_GENERATION_ROUTING_KEY = DEFAULT_PRIORITY_QUEUE
CREDENTIALS_COURSE_COMPLETION_STATE = 'awarded'

# Queue to use for award program certificates
PROGRAM_CERTIFICATES_ROUTING_KEY = 'edx.lms.core.default'

# Settings for Comprehensive Theming app

# See https://github.com/openedx/edx-django-sites-extensions for more info
# Default site to use if site matching request headers does not exist
SITE_ID = 1

# .. setting_name: COMPREHENSIVE_THEME_DIRS
# .. setting_default: []
# .. setting_description: A list of paths to directories, each of which will
#   be searched for comprehensive themes. Do not override this Django setting directly.
#   Instead, set the COMPREHENSIVE_THEME_DIRS environment variable, using colons (:) to
#   separate paths.
COMPREHENSIVE_THEME_DIRS = os.environ.get("COMPREHENSIVE_THEME_DIRS", "").split(":")

# .. setting_name: COMPREHENSIVE_THEME_LOCALE_PATHS
# .. setting_default: []
# .. setting_description: A list of the paths to themes locale directories e.g.
#   "COMPREHENSIVE_THEME_LOCALE_PATHS" : ["/edx/src/edx-themes/conf/locale"].
COMPREHENSIVE_THEME_LOCALE_PATHS = []


# .. setting_name: PREPEND_LOCALE_PATHS
# .. setting_default: []
# .. setting_description: A list of the paths to locale directories to load first e.g.
#   "PREPEND_LOCALE_PATHS" : ["/edx/my-locales/"].
PREPEND_LOCALE_PATHS = []

# .. setting_name: DEFAULT_SITE_THEME
# .. setting_default: None
# .. setting_description: Theme to use when no site or site theme is defined, for example
#   "dark-theme". Set to None if you want to use openedx default theme.
# .. setting_warning: The theme folder needs to be in 'edx-platform/themes' or define the path
#   to the theme folder in COMPREHENSIVE_THEME_DIRS. To be effective, ENABLE_COMPREHENSIVE_THEMING
#   has to be enabled.
DEFAULT_SITE_THEME = None

# .. toggle_name: ENABLE_COMPREHENSIVE_THEMING
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When enabled, this toggle activates the use of the custom theme
#   defined by DEFAULT_SITE_THEME.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2016-06-30
ENABLE_COMPREHENSIVE_THEMING = False

# .. setting_name: CUSTOM_RESOURCE_TEMPLATES_DIRECTORY
# .. setting_default: None
# .. setting_description: Path to an existing directory of YAML files containing
#    html content to be used with the subclasses of xmodule.x_module.ResourceTemplates.
#    Default example templates can be found in xmodule/templates/html.
#    Note that the extension used is ".yaml" and not ".yml".
#    See xmodule.x_module.ResourceTemplates for usage.
#   "CUSTOM_RESOURCE_TEMPLATES_DIRECTORY" : null
CUSTOM_RESOURCE_TEMPLATES_DIRECTORY = None

# API access management
API_ACCESS_MANAGER_EMAIL = 'api-access@example.com'
API_ACCESS_FROM_EMAIL = 'api-requests@example.com'
API_DOCUMENTATION_URL = 'https://course-catalog-api-guide.readthedocs.io/en/latest/'
AUTH_DOCUMENTATION_URL = 'https://course-catalog-api-guide.readthedocs.io/en/latest/authentication/index.html'

# Affiliate cookie tracking
AFFILIATE_COOKIE_NAME = 'dev_affiliate_id'

############## Settings for RedirectMiddleware ###############

# Setting this to None causes Redirect data to never expire
# The cache is cleared when Redirect models are saved/deleted
REDIRECT_CACHE_TIMEOUT = None  # The length of time we cache Redirect model data
REDIRECT_CACHE_KEY_PREFIX = 'redirects'

############## Settings for LMS Context Sensitive Help ##############

HELP_TOKENS_INI_FILE = REPO_ROOT / "lms" / "envs" / "help_tokens.ini"
HELP_TOKENS_LANGUAGE_CODE = lambda settings: settings.LANGUAGE_CODE
HELP_TOKENS_VERSION = lambda settings: doc_version()
HELP_TOKENS_BOOKS = {
    'learner': 'https://edx.readthedocs.io/projects/open-edx-learner-guide',
    'course_author': 'https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course',
}
derived('HELP_TOKENS_LANGUAGE_CODE', 'HELP_TOKENS_VERSION')

############## OPEN EDX ENTERPRISE SERVICE CONFIGURATION ######################
# The Open edX Enterprise service is currently hosted via the LMS container/process.
# However, for all intents and purposes this service is treated as a standalone IDA.
# These configuration settings are specific to the Enterprise service and you should
# not find references to them within the edx-platform project.
#
# Only used if FEATURES['ENABLE_ENTERPRISE_INTEGRATION'] == True.

ENTERPRISE_ENROLLMENT_API_URL = LMS_INTERNAL_ROOT_URL + LMS_ENROLLMENT_API_PATH
ENTERPRISE_PUBLIC_ENROLLMENT_API_URL = LMS_ROOT_URL + LMS_ENROLLMENT_API_PATH
ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES = ['audit', 'honor']
ENTERPRISE_SUPPORT_URL = ''
ENTERPRISE_CUSTOMER_CATALOG_DEFAULT_CONTENT_FILTER = {}
ENTERPRISE_CUSTOMER_SUCCESS_EMAIL = "customersuccess@edx.org"
ENTERPRISE_INTEGRATIONS_EMAIL = "enterprise-integrations@edx.org"


# The setting key maps to the channel code (e.g. 'SAP' for success factors), Channel code is defined as
# part of django model of each integrated channel in edx-enterprise.
# The absence of a key/value pair translates to NO LIMIT on the number of "chunks" transmitted per cycle.
INTEGRATED_CHANNELS_API_CHUNK_TRANSMISSION_LIMIT = {}

############## ENTERPRISE SERVICE API CLIENT CONFIGURATION ######################
# The LMS communicates with the Enterprise service via the requests.Session() client
# These default settings are utilized by the LMS when interacting with the service,
# and are overridden by the configuration parameter accessors defined in production.py

ENTERPRISE_API_URL = 'https://localhost:18000/enterprise/api/v1'
ENTERPRISE_CONSENT_API_URL = LMS_INTERNAL_ROOT_URL + '/consent/api/v1/'
ENTERPRISE_SERVICE_WORKER_USERNAME = 'enterprise_worker'
ENTERPRISE_API_CACHE_TIMEOUT = 3600  # Value is in seconds
ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE = 512   # Enterprise logo image size limit in KB's
ENTERPRISE_CATALOG_INTERNAL_ROOT_URL = 'http://enterprise.catalog.app:18160'
# Defines the usernames of service users who should be throttled
# at a higher rate than normal users when making requests of enterprise endpoints.
ENTERPRISE_ALL_SERVICE_USERNAMES = [
    'ecommerce_worker',
    'enterprise_worker',
    'license_manager_worker',
    'enterprise_catalog_worker',
    'enterprise_channel_worker',
    'enterprise_access_worker',
    'enterprise_subsidy_worker',
    'subscriptions_worker'
]

# Setting for Open API key and prompts used by edx-enterprise.
CHAT_COMPLETION_API = 'https://example.com/chat/completion'
CHAT_COMPLETION_API_KEY = 'i am a key'
LEARNER_ENGAGEMENT_PROMPT_FOR_ACTIVE_CONTRACT = ''
LEARNER_ENGAGEMENT_PROMPT_FOR_NON_ACTIVE_CONTRACT = ''
LEARNER_PROGRESS_PROMPT_FOR_ACTIVE_CONTRACT = ''
LEARNER_PROGRESS_PROMPT_FOR_NON_ACTIVE_CONTRACT = ''


############## ENTERPRISE SERVICE LMS CONFIGURATION ##################################
# The LMS has some features embedded that are related to the Enterprise service, but
# which are not provided by the Enterprise service. These settings provide base values
# for those features.

ENTERPRISE_PLATFORM_WELCOME_TEMPLATE = _('Welcome to {platform_name}.')
ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE = _(
    'You have left the {start_bold}{enterprise_name}{end_bold} website and are now on the {platform_name} site. '
    '{enterprise_name} has partnered with {platform_name} to offer you high-quality, always available learning '
    'programs to help you advance your knowledge and career. '
    '{line_break}Please note that {platform_name} has a different {privacy_policy_link_start}Privacy Policy'
    '{privacy_policy_link_end} from {enterprise_name}.'
)
ENTERPRISE_PROXY_LOGIN_WELCOME_TEMPLATE = _(
    '{start_bold}{enterprise_name}{end_bold} has partnered with {start_bold}{platform_name}{end_bold} '
    'to offer you high-quality learning opportunities from the world\'s best institutions and universities.'
)
ENTERPRISE_TAGLINE = ''
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS = {
    'age',
    'level_of_education',
    'gender',
    'goals',
    'year_of_birth',
    'mailing_address',
}
ENTERPRISE_READONLY_ACCOUNT_FIELDS = [
    'username',
    'name',
    'email',
    'country',
]
ENTERPRISE_CUSTOMER_COOKIE_NAME = 'enterprise_customer_uuid'
BASE_COOKIE_DOMAIN = 'localhost'
SYSTEM_TO_FEATURE_ROLE_MAPPING = {
    ENTERPRISE_ADMIN_ROLE: [
        ENTERPRISE_DASHBOARD_ADMIN_ROLE,
        ENTERPRISE_CATALOG_ADMIN_ROLE,
        ENTERPRISE_ENROLLMENT_API_ADMIN_ROLE,
        ENTERPRISE_REPORTING_CONFIG_ADMIN_ROLE,
    ],
    ENTERPRISE_OPERATOR_ROLE: [
        ENTERPRISE_DASHBOARD_ADMIN_ROLE,
        ENTERPRISE_CATALOG_ADMIN_ROLE,
        ENTERPRISE_ENROLLMENT_API_ADMIN_ROLE,
        ENTERPRISE_REPORTING_CONFIG_ADMIN_ROLE,
        ENTERPRISE_FULFILLMENT_OPERATOR_ROLE,
        ENTERPRISE_SSO_ORCHESTRATOR_OPERATOR_ROLE,
    ],
    SYSTEM_ENTERPRISE_PROVISIONING_ADMIN_ROLE: [
        PROVISIONING_ENTERPRISE_CUSTOMER_ADMIN_ROLE,
        PROVISIONING_PENDING_ENTERPRISE_CUSTOMER_ADMIN_ROLE,
    ],
}

DATA_CONSENT_SHARE_CACHE_TIMEOUT = 8 * 60 * 60  # 8 hours

ENTERPRISE_MARKETING_FOOTER_QUERY_PARAMS = {}
ENTERPRISE_TAGLINE = ''

############## Settings for Course Enrollment Modes ######################
# The min_price key refers to the minimum price allowed for an instance
# of a particular type of course enrollment mode. This is not to be confused
# with the min_price field of the CourseMode model, which refers to the actual
# price of the CourseMode.
COURSE_ENROLLMENT_MODES = {
    "audit": {
        "id": 1,
        "slug": "audit",
        "display_name": _("Audit"),
        "min_price": 0,
    },
    "verified": {
        "id": 2,
        "slug": "verified",
        "display_name": _("Verified"),
        "min_price": 1,
    },
    "professional": {
        "id": 3,
        "slug": "professional",
        "display_name": _("Professional"),
        "min_price": 1,
    },
    "no-id-professional": {
        "id": 4,
        "slug": "no-id-professional",
        "display_name": _("No-Id-Professional"),
        "min_price": 0,
    },
    "credit": {
        "id": 5,
        "slug": "credit",
        "display_name": _("Credit"),
        "min_price": 0,
    },
    "honor": {
        "id": 6,
        "slug": "honor",
        "display_name": _("Honor"),
        "min_price": 0,
    },
    "masters": {
        "id": 7,
        "slug": "masters",
        "display_name": _("Master's"),
        "min_price": 0,
    },
    "executive-education": {
        "id": 8,
        "slug": "executive-educations",
        "display_name": _("Executive Education"),
        "min_price": 1
    },
    "unpaid-executive-education": {
        "id": 9,
        "slug": "unpaid-executive-education",
        "display_name": _("Unpaid Executive Education"),
        "min_price": 0
    },
    "paid-executive-education": {
        "id": 10,
        "slug": "paid-executive-education",
        "display_name": _("Paid Executive Education"),
        "min_price": 1
    },
    "unpaid-bootcamp": {
        "id": 11,
        "slug": "unpaid-bootcamp",
        "display_name": _("Unpaid Bootcamp"),
        "min_price": 0
    },
    "paid-bootcamp": {
        "id": 12,
        "slug": "paid-bootcamp",
        "display_name": _("Paid Bootcamp"),
        "min_price": 1
    },
}

CONTENT_TYPE_GATE_GROUP_IDS = {
    'limited_access': 1,
    'full_access': 2,
}

############## Settings for the Discovery App ######################

COURSES_API_CACHE_TIMEOUT = 3600  # Value is in seconds


# Initialize to 'unknown', but read from JSON in production.py
EDX_PLATFORM_REVISION = 'release'

############## Settings for Completion API #########################

# Once a user has watched this percentage of a video, mark it as complete:
# (0.0 = 0%, 1.0 = 100%)
COMPLETION_VIDEO_COMPLETE_PERCENTAGE = 0.95
COMPLETION_BY_VIEWING_DELAY_MS = 5000

############### Settings for Django Rate limit #####################

# .. toggle_name: RATELIMIT_ENABLE
# .. toggle_implementation: DjangoSetting
# .. toggle_default: True
# .. toggle_description: When enabled, RATELIMIT_RATE is applied.
#    When disabled, RATELIMIT_RATE is not applied.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2018-01-08
# .. toggle_tickets: https://github.com/openedx/edx-platform/pull/16951
RATELIMIT_ENABLE = True

# .. setting_name: RATELIMIT_RATE
# .. setting_default: 120/m
# .. setting_description: Due to some reports about attack on /oauth2/access_token/ which took LMS down,
#    this setting was introduced to rate-limit all endpoints of AccessTokenView up to
#    120 requests per IP Address in a minute by default.
# .. setting_warning: RATELIMIT_ENABLE flag must also be enabled/set to True to use this RATELIMIT_RATE setting.
# .. setting_use_cases: open_edx
# .. setting_creation_date: 2018-01-08
# .. setting_tickets: https://github.com/openedx/edx-platform/pull/16951
RATELIMIT_RATE = '120/m'

##### LOGISTRATION RATE LIMIT SETTINGS #####
LOGISTRATION_RATELIMIT_RATE = '100/5m'
LOGISTRATION_PER_EMAIL_RATELIMIT_RATE = '30/5m'
LOGISTRATION_API_RATELIMIT = '20/m'
LOGIN_AND_REGISTER_FORM_RATELIMIT = '100/5m'
RESET_PASSWORD_TOKEN_VALIDATE_API_RATELIMIT = '30/7d'
RESET_PASSWORD_API_RATELIMIT = '30/7d'
OPTIONAL_FIELD_API_RATELIMIT = '10/h'

##### PASSWORD RESET RATE LIMIT SETTINGS #####
PASSWORD_RESET_IP_RATE = '1/m'
PASSWORD_RESET_EMAIL_RATE = '2/h'


#### BRAZE API SETTINGS ####

EDX_BRAZE_API_KEY = None
EDX_BRAZE_API_SERVER = None
BRAZE_COURSE_ENROLLMENT_CANVAS_ID = ''

# Keeping this for back compatibility with learner dashboard api
GENERAL_RECOMMENDATION = {}

############### Settings for Retirement #####################
# .. setting_name: RETIRED_USERNAME_PREFIX
# .. setting_default: retired__user_
# .. setting_description: Set the prefix part of hashed usernames for retired users. Used by the derived
#     setting RETIRED_USERNAME_FMT.
RETIRED_USERNAME_PREFIX = 'retired__user_'
# .. setting_name: RETIRED_EMAIL_PREFIX
# .. setting_default: retired__user_
# .. setting_description: Set the prefix part of hashed emails for retired users. Used by the derived
#     setting RETIRED_EMAIL_FMT.
RETIRED_EMAIL_PREFIX = 'retired__user_'
# .. setting_name: RETIRED_EMAIL_DOMAIN
# .. setting_default: retired.invalid
# .. setting_description: Set the domain part of hashed emails for retired users. Used by the derived
#     setting RETIRED_EMAIL_FMT.
RETIRED_EMAIL_DOMAIN = 'retired.invalid'
# .. setting_name: RETIRED_USERNAME_FMT
# .. setting_default: retired__user_{}
# .. setting_description: Set the format a retired user username field gets transformed into, where {}
#     is replaced with the hash of the original username. This is a derived setting that depends on
#     RETIRED_USERNAME_PREFIX value.
RETIRED_USERNAME_FMT = lambda settings: settings.RETIRED_USERNAME_PREFIX + '{}'
# .. setting_name: RETIRED_EMAIL_FMT
# .. setting_default: retired__user_{}@retired.invalid
# .. setting_description: Set the format a retired user email field gets transformed into, where {} is
#     replaced with the hash of the original email. This is a derived setting that depends on
#     RETIRED_EMAIL_PREFIX and RETIRED_EMAIL_DOMAIN values.
RETIRED_EMAIL_FMT = lambda settings: settings.RETIRED_EMAIL_PREFIX + '{}@' + settings.RETIRED_EMAIL_DOMAIN
derived('RETIRED_USERNAME_FMT', 'RETIRED_EMAIL_FMT')
# .. setting_name: RETIRED_USER_SALTS
# .. setting_default: ['abc', '123']
# .. setting_description: Set a list of salts used for hashing usernames and emails on users retirement.
# .. setting_warning: Only the last item in this list is used as a salt for all new retirements, but
#     historical salts are preserved in order to guarantee that all hashed usernames and emails can still
#     be checked.
RETIRED_USER_SALTS = ['abc', '123']
# .. setting_name: RETIREMENT_SERVICE_WORKER_USERNAME
# .. setting_default: RETIREMENT_SERVICE_USER
# .. setting_description: Set the username of the retirement service worker user. Retirement scripts
#     authenticate with LMS as this user with oauth client credentials.
RETIREMENT_SERVICE_WORKER_USERNAME = 'RETIREMENT_SERVICE_USER'

# These states are the default, but are designed to be overridden in configuration.
# .. setting_name: RETIREMENT_STATES
# .. setting_default:
#     [
#         'PENDING',
#         'LOCKING_ACCOUNT',
#         'LOCKING_COMPLETE',
#         'RETIRING_FORUMS',
#         'FORUMS_COMPLETE',
#         'RETIRING_EMAIL_LISTS',
#         'EMAIL_LISTS_COMPLETE',
#         'RETIRING_ENROLLMENTS',
#         'ENROLLMENTS_COMPLETE',
#         'RETIRING_NOTES',
#         'NOTES_COMPLETE',
#         'RETIRING_LMS',
#         'LMS_COMPLETE',
#         'ERRORED',
#         'ABORTED',
#         'COMPLETE',
#     ]
# .. setting_description: Set a list that defines the name and order of states for the retirement
#     workflow.
# .. setting_warning: These states are stored in the database and it is the responsibility of the
#     administrator to populate the state list since the states can vary across different installations.
#     There must be, at minimum, a PENDING state at the beginning, and COMPLETED, ERRORED, and ABORTED
#     states at the end of the list.
RETIREMENT_STATES = [
    'PENDING',

    'LOCKING_ACCOUNT',
    'LOCKING_COMPLETE',

    # Use these states only when ENABLE_DISCUSSION_SERVICE is True.
    'RETIRING_FORUMS',
    'FORUMS_COMPLETE',

    # TODO - Change these states to be the LMS-only email opt-out - PLAT-2189
    'RETIRING_EMAIL_LISTS',
    'EMAIL_LISTS_COMPLETE',

    'RETIRING_ENROLLMENTS',
    'ENROLLMENTS_COMPLETE',

    # Use these states only when ENABLE_STUDENT_NOTES is True.
    'RETIRING_NOTES',
    'NOTES_COMPLETE',

    'RETIRING_LMS',
    'LMS_COMPLETE',

    'ERRORED',
    'ABORTED',
    'COMPLETE',
]

USERNAME_REPLACEMENT_WORKER = "REPLACE WITH VALID USERNAME"

############## Settings for Microfrontends  #########################
# If running a Gradebook container locally,
# modify lms/envs/private.py to give it a non-null value
WRITABLE_GRADEBOOK_URL = None
# .. setting_name: PROFILE_MICROFRONTEND_URL
# .. setting_default: None
# .. setting_description: Base URL of the micro-frontend-based profile page.
# .. setting_warning: Also set site's ENABLE_PROFILE_MICROFRONTEND and
#     learner_profile.redirect_to_microfrontend waffle flag
PROFILE_MICROFRONTEND_URL = None
ORDER_HISTORY_MICROFRONTEND_URL = None
# .. setting_name: ACCOUNT_MICROFRONTEND_URL
# .. setting_default: None
# .. setting_description: Base URL of the micro-frontend-based account settings page.
# .. setting_warning: Also set site's ENABLE_ACCOUNT_MICROFRONTEND and
#     account.redirect_to_microfrontend waffle flag
ACCOUNT_MICROFRONTEND_URL = None
AUTHN_MICROFRONTEND_URL = None
AUTHN_MICROFRONTEND_DOMAIN = None
PROGRAM_CONSOLE_MICROFRONTEND_URL = None
# .. setting_name: LEARNING_MICROFRONTEND_URL
# .. setting_default: None
# .. setting_description: Base URL of the micro-frontend-based courseware page.
LEARNING_MICROFRONTEND_URL = None
# .. setting_name: ORA_GRADING_MICROFRONTEND_URL
# .. setting_default: None
# .. setting_description: Base URL of the micro-frontend-based openassessment grading page.
#     This is will be show in the open response tab list data.
# .. setting_warning: Also set site's openresponseassessment.enhanced_staff_grader
#     waffle flag.
ORA_GRADING_MICROFRONTEND_URL = None
# .. setting_name: ORA_MICROFRONTEND_URL
# .. setting_default: None
# .. setting_description: Base URL for modern openassessment app.
#     This is will be show in the open response tab list data.
# .. setting_warning: Also set site's openresponseassessment.mfe_views
#     waffle flag.
ORA_MICROFRONTEND_URL = None
# .. setting_name: DISCUSSIONS_MICROFRONTEND_URL
# .. setting_default: None
# .. setting_description: Base URL of the micro-frontend-based discussions page.
# .. setting_warning: Also set site's courseware.discussions_mfe waffle flag.
DISCUSSIONS_MICROFRONTEND_URL = None
# .. setting_name: DISCUSSIONS_MFE_FEEDBACK_URL
# .. setting_default: None
# .. setting_description: Base URL of the discussions micro-frontend google form based feedback.
DISCUSSIONS_MFE_FEEDBACK_URL = None
# .. setting_name: EXAMS_DASHBOARD_MICROFRONTEND_URL
# .. setting_default: None
# .. setting_description: Base URL of the exams dashboard micro-frontend for instructors.
EXAMS_DASHBOARD_MICROFRONTEND_URL = None
# .. toggle_name: ENABLE_AUTHN_RESET_PASSWORD_HIBP_POLICY
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When enabled, this toggle activates the use of the password validation
#   HIBP Policy.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2021-12-03
# .. toggle_tickets: https://openedx.atlassian.net/browse/VAN-666
ENABLE_AUTHN_RESET_PASSWORD_HIBP_POLICY = False
# .. toggle_name: ENABLE_AUTHN_REGISTER_HIBP_POLICY
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When enabled, this toggle activates the use of the password validation
#   HIBP Policy on Authn MFE's registration.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2022-03-25
# .. toggle_tickets: https://openedx.atlassian.net/browse/VAN-669
ENABLE_AUTHN_REGISTER_HIBP_POLICY = False
HIBP_REGISTRATION_PASSWORD_FREQUENCY_THRESHOLD = 3

# .. toggle_name: ENABLE_AUTHN_LOGIN_NUDGE_HIBP_POLICY
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When enabled, this toggle activates the use of the password validation
#   on Authn MFE's login.
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2022-03-29
# .. toggle_target_removal_date: None
# .. toggle_tickets: https://openedx.atlassian.net/browse/VAN-668
ENABLE_AUTHN_LOGIN_NUDGE_HIBP_POLICY = False
HIBP_LOGIN_NUDGE_PASSWORD_FREQUENCY_THRESHOLD = 3

# .. toggle_name: ENABLE_AUTHN_LOGIN_BLOCK_HIBP_POLICY
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When enabled, this toggle activates the use of the password validation
#   on Authn MFE's login.
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2022-03-29
# .. toggle_target_removal_date: None
# .. toggle_tickets: https://openedx.atlassian.net/browse/VAN-667
ENABLE_AUTHN_LOGIN_BLOCK_HIBP_POLICY = False
HIBP_LOGIN_BLOCK_PASSWORD_FREQUENCY_THRESHOLD = 5

# .. toggle_name: ENABLE_DYNAMIC_REGISTRATION_FIELDS
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When enabled, this toggle adds fields configured in
# REGISTRATION_EXTRA_FIELDS to Authn MFE
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2022-04-21
# .. toggle_target_removal_date: None
# .. toggle_tickets: https://openedx.atlassian.net/browse/VAN-838
ENABLE_DYNAMIC_REGISTRATION_FIELDS = False

############## Settings for EmailChangeMiddleware ###############

# .. toggle_name: ENFORCE_SESSION_EMAIL_MATCH
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: When enabled, this setting invalidates sessions in other browsers
#       upon email change, while preserving the session validity in the browser where the
#       email change occurs. This toggle is just being used for rollout.
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2023-12-07
# .. toggle_target_removal_date: 2024-04-01
# .. toggle_tickets: https://2u-internal.atlassian.net/browse/VAN-1797
ENFORCE_SESSION_EMAIL_MATCH = False

############### Settings for the ace_common plugin #################
# Note that all settings are actually defined by the plugin
# pylint: disable=wrong-import-position
from openedx.core.djangoapps.ace_common.settings import common as ace_common_settings
ACE_ROUTING_KEY = ace_common_settings.ACE_ROUTING_KEY

############### Settings swift #####################################
SWIFT_USERNAME = None
SWIFT_KEY = None
SWIFT_TENANT_ID = None
SWIFT_TENANT_NAME = None
SWIFT_AUTH_URL = None
SWIFT_AUTH_VERSION = None
SWIFT_REGION_NAME = None
SWIFT_USE_TEMP_URLS = None
SWIFT_TEMP_URL_KEY = None
SWIFT_TEMP_URL_DURATION = 1800  # seconds

############### Settings for facebook ##############################
FACEBOOK_APP_ID = 'FACEBOOK_APP_ID'
FACEBOOK_APP_SECRET = 'FACEBOOK_APP_SECRET'
FACEBOOK_API_VERSION = 'v2.1'

############### Settings for django-fernet-fields ##################
FERNET_KEYS = [
    'DUMMY KEY CHANGE BEFORE GOING TO PRODUCTION',
]

############### Settings for user-state-client ##################
# Maximum number of rows to fetch in XBlockUserStateClient calls. Adjust for performance
USER_STATE_BATCH_SIZE = 5000

############### Settings for edx-rbac  ###############
SYSTEM_WIDE_ROLE_CLASSES = []

############## Plugin Django Apps #########################

from edx_django_utils.plugins import get_plugin_apps, add_plugins  # pylint: disable=wrong-import-position,wrong-import-order
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType  # pylint: disable=wrong-import-position
INSTALLED_APPS.extend(get_plugin_apps(ProjectType.LMS))
add_plugins(__name__, ProjectType.LMS, SettingsType.COMMON)

DEPRECATED_ADVANCED_COMPONENT_TYPES = []

############### Settings for video pipeline ##################
VIDEO_UPLOAD_PIPELINE = {
    'VEM_S3_BUCKET': '',
    'BUCKET': '',
    'ROOT_PATH': '',
}

############### Settings for django file storage ##################
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

### Proctoring configuration (redirct URLs and keys shared between systems) ####
PROCTORING_BACKENDS = {
    'DEFAULT': 'null',
    # The null key needs to be quoted because
    # null is a language independent type in YAML
    'null': {}
}

PROCTORED_EXAM_VIEWABLE_PAST_DUE = False

############### The SAML private/public key values ################
SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = ""
SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = ""
SOCIAL_AUTH_SAML_SP_PRIVATE_KEY_DICT = {}
SOCIAL_AUTH_SAML_SP_PUBLIC_CERT_DICT = {}

######################### rate limit for yt_video_metadata api ##############

RATE_LIMIT_FOR_VIDEO_METADATA_API = '10/minute'

########################## MAILCHIMP SETTINGS #################################
MAILCHIMP_NEW_USER_LIST_ID = ""

SYSLOG_SERVER = ''
FEEDBACK_SUBMISSION_EMAIL = ''
GITHUB_REPO_ROOT = '/edx/var/edxapp/data'

##################### SUPPORT URL ############################
SUPPORT_HOW_TO_UNENROLL_LINK = ''

######################## Setting for content libraries ########################
MAX_BLOCKS_PER_CONTENT_LIBRARY = 1000

######################## Setting for django-countries ########################
# django-countries provides an option to make the desired countries come up in
# selection forms, if left empty countries will come up in ascending order as before.
# This accepts a list of ISO3166-1 two letter country code, For example,
# COUNTRIES_FIRST = ['SA', 'BH', 'QA'] will display these countries on top of the list
# https://github.com/SmileyChris/django-countries#show-certain-countries-first
COUNTRIES_FIRST = []

################# Settings for brand logos. #################
LOGO_IMAGE_EXTRA_TEXT = ''
LOGO_URL = None
LOGO_URL_PNG = None
LOGO_TRADEMARK_URL = None
FAVICON_URL = None
DEFAULT_EMAIL_LOGO_URL = 'https://edx-cdn.org/v3/default/logo.png'

################# Settings for olx validation. #################
COURSE_OLX_VALIDATION_STAGE = 1
COURSE_OLX_VALIDATION_IGNORE_LIST = None

################# show account activate cta after register ########################
SHOW_ACTIVATE_CTA_POPUP_COOKIE_NAME = 'show-account-activation-popup'
# .. toggle_name: SOME_FEATURE_NAME
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: Flag would be used to show account activation popup after the registration
# .. toggle_use_cases: open_edx
# .. toggle_tickets: https://github.com/openedx/edx-platform/pull/27661
# .. toggle_creation_date: 2021-06-10
SHOW_ACCOUNT_ACTIVATION_CTA = False

################# Documentation links for course apps #################

# pylint: disable=line-too-long
CALCULATOR_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/exercises_tools/calculator.html"
DISCUSSIONS_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/course_components/create_discussion.html"
EDXNOTES_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/exercises_tools/notes.html"
PROGRESS_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/course_assets/pages.html?highlight=progress#hiding-or-showing-the-wiki-or-progress-pages"
TEAMS_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/course_features/teams/teams_setup.html"
TEXTBOOKS_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/course_assets/textbooks.html"
WIKI_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/course_assets/course_wiki.html"
CUSTOM_PAGES_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/course_assets/pages.html#adding-custom-pages"
COURSE_BULK_EMAIL_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/manage_live_course/bulk_email.html"
ORA_SETTINGS_HELP_URL = "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/course_assets/pages.html#configuring-course-level-open-response-assessment-settings"

################# Bulk Course Email Settings #################
# If set, recipients of bulk course email messages will be filtered based on the last_login date of their User account.
# The expected value is an Integer representing the cutoff point (in months) for inclusion to the message. Example:
# a value of `3` would include learners who have logged in within the past 3 months.
BULK_COURSE_EMAIL_LAST_LOGIN_ELIGIBILITY_PERIOD = None

################ Settings for the Discussion Service #########
# Provide a list of reason codes for moderators editing posts and
# comments, as a mapping from the internal reason code representation,
# to an internationalizable label to be shown to moderators in the form UI.
DISCUSSION_MODERATION_EDIT_REASON_CODES = {
    "grammar-spelling": _("Has grammar / spelling issues"),
    "needs-clarity": _("Content needs clarity"),
    "academic-integrity": _("Has academic integrity concern"),
    "inappropriate-language": _("Has inappropriate language"),
    "format-change": _("Formatting changes needed"),
    "post-type-change": _("Post type needs change"),
    "contains-pii": _("Contains personally identifiable information"),
    "violates-guidelines": _("Violates community guidelines"),
}
# Provide a list of reason codes for moderators to close posts, as a mapping
# from the internal reason code representation, to  an internationalizable label
#  to be shown to moderators in the form UI.
DISCUSSION_MODERATION_CLOSE_REASON_CODES = {
    "academic-integrity": _("Post violates honour code or academic integrity"),
    "read-only": _("Post should be read-only"),
    "duplicate": _("Post is a duplicate"),
    "off-topic": _("Post is off-topic"),
}

################# Settings for edx-financial-assistance #################
IS_ELIGIBLE_FOR_FINANCIAL_ASSISTANCE_URL = '/core/api/course_eligibility/'
FINANCIAL_ASSISTANCE_APPLICATION_STATUS_URL = "/core/api/financial_assistance_application/status/"
CREATE_FINANCIAL_ASSISTANCE_APPLICATION_URL = '/core/api/financial_assistance_applications'

######################## Enterprise API Client ########################
ENTERPRISE_BACKEND_SERVICE_EDX_OAUTH2_KEY = "enterprise-backend-service-key"
ENTERPRISE_BACKEND_SERVICE_EDX_OAUTH2_SECRET = "enterprise-backend-service-secret"
ENTERPRISE_BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://127.0.0.1:8000/oauth2"

# keys for  big blue button live provider
COURSE_LIVE_GLOBAL_CREDENTIALS = {}

# .. toggle_name: ENABLE_MFE_CONFIG_API
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: Set to True to enable MFE Config API. This is disabled by
#   default.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2022-05-20
# .. toggle_target_removal_date: None
# .. toggle_warnings: None
# .. toggle_tickets: None
ENABLE_MFE_CONFIG_API = False

# .. setting_name: MFE_CONFIG
# .. setting_implementation: DjangoSetting
# .. setting_default: {}
# .. setting_description: Is a configuration that will be exposed by the MFE Config API to be consumed by the MFEs.
#   Contains configuration common to all MFEs. When a specific MFE's configuration is requested, these values
#   will be treated as a base and then overriden/supplemented by those in `MFE_CONFIG_OVERRIDES`.
#   Example: {
#     "BASE_URL": "https://name_of_mfe.example.com",
#     "LANGUAGE_PREFERENCE_COOKIE_NAME": "example-language-preference",
#     "CREDENTIALS_BASE_URL": "https://credentials.example.com",
#     "DISCOVERY_API_BASE_URL": "https://discovery.example.com",
#     "LMS_BASE_URL": "https://courses.example.com",
#     "LOGIN_URL": "https://courses.example.com/login",
#     "LOGOUT_URL": "https://courses.example.com/logout",
#     "STUDIO_BASE_URL": "https://studio.example.com",
#     "LOGO_URL": "https://courses.example.com/logo.png"
#   }
# .. setting_use_cases: open_edx
# .. setting_creation_date: 2022-08-05
MFE_CONFIG = {}

# .. setting_name: MFE_CONFIG_OVERRIDES
# .. setting_implementation: DjangoSetting
# .. setting_default: {}
# .. setting_description: Overrides or additions to `MFE_CONFIG` for when a specific MFE is requested
#   by the MFE Config API. Top-level keys are APP_IDs, a.k.a. the name of the MFE (for example,
#   for an MFE named "frontend-app-xyz", the top-level key would be "xyz").
#   Example: {
#     "gradebook": {
#        "BASE_URL": "https://gradebook.example.com",
#     },
#     "profile": {
#        "BASE_URL": "https://profile.example.com",
#        "ENABLE_LEARNER_RECORD_MFE": "true",
#     },
#   }
# .. setting_use_cases: open_edx
# .. setting_creation_date: 2022-08-05
MFE_CONFIG_OVERRIDES = {}

# .. setting_name: MFE_CONFIG_API_CACHE_TIMEOUT
# .. setting_default: 60*5
# .. setting_description: The MFE Config API response will be cached during the
#   specified time
MFE_CONFIG_API_CACHE_TIMEOUT = 60 * 5

######################## Settings for Outcome Surveys plugin ########################
OUTCOME_SURVEYS_EVENTS_ENABLED = True

######################## Settings for cancel retirement in Support Tools ########################
COOL_OFF_DAYS = 14

############ Settings for externally hosted executive education courses ############
EXEC_ED_LANDING_PAGE = "https://www.getsmarter.com/account"

############## PLOTLY ##############

ENTERPRISE_PLOTLY_SECRET = "I am a secret"

############## PLOTLY ##############

############ Internal Enterprise Settings ############
ENTERPRISE_VSF_UUID = "e815503343644ac7845bc82325c34460"
############ Internal Enterprise Settings ############

ENTERPRISE_MANUAL_REPORTING_CUSTOMER_UUIDS = []

AVAILABLE_DISCUSSION_TOURS = []

######################## Subscriptions API SETTINGS ########################
SUBSCRIPTIONS_ROOT_URL = ""
SUBSCRIPTIONS_API_PATH = f"{SUBSCRIPTIONS_ROOT_URL}/api/v1/stripe-subscription/"

SUBSCRIPTIONS_LEARNER_HELP_CENTER_URL = None
SUBSCRIPTIONS_BUY_SUBSCRIPTION_URL = f"{SUBSCRIPTIONS_ROOT_URL}/api/v1/stripe-subscribe/"
SUBSCRIPTIONS_MANAGE_SUBSCRIPTION_URL = None
SUBSCRIPTIONS_MINIMUM_PRICE = '$39'
SUBSCRIPTIONS_TRIAL_LENGTH = 7
SUBSCRIPTIONS_SERVICE_WORKER_USERNAME = 'subscriptions_worker'

############## NOTIFICATIONS ##############
NOTIFICATIONS_EXPIRY = 60
EXPIRED_NOTIFICATIONS_DELETE_BATCH_SIZE = 10000
NOTIFICATION_CREATION_BATCH_SIZE = 76
NOTIFICATIONS_DEFAULT_FROM_EMAIL = "no-reply@example.com"
NOTIFICATION_TYPE_ICONS = {}
DEFAULT_NOTIFICATION_ICON_URL = ""

############################ AI_TRANSLATIONS ##################################
AI_TRANSLATIONS_API_URL = 'http://localhost:18760/api/v1'

#### django-simple-history##
# disable indexing on date field its coming from django-simple-history.
SIMPLE_HISTORY_DATE_INDEX = False


def _should_send_certificate_events(settings):
    return settings.FEATURES['SEND_LEARNING_CERTIFICATE_LIFECYCLE_EVENTS_TO_BUS']


#### Event bus producing ####

def _should_send_learning_badge_events(settings):
    return settings.FEATURES['BADGES_ENABLED']

# .. setting_name: EVENT_BUS_PRODUCER_CONFIG
# .. setting_default: all events disabled
# .. setting_description: Dictionary of event_types mapped to dictionaries of topic to topic-related configuration.
#    Each topic configuration dictionary contains
#    * `enabled`: a toggle denoting whether the event will be published to the topic. These should be annotated
#       according to
#       https://edx.readthedocs.io/projects/edx-toggles/en/latest/how_to/documenting_new_feature_toggles.html
#    * `event_key_field` which is a period-delimited string path to event data field to use as event key.
#    Note: The topic names should not include environment prefix as it will be dynamically added based on
#    EVENT_BUS_TOPIC_PREFIX setting.
EVENT_BUS_PRODUCER_CONFIG = {
    'org.openedx.learning.certificate.created.v1': {
        'learning-certificate-lifecycle':
            {'event_key_field': 'certificate.course.course_key', 'enabled': _should_send_certificate_events},
    },
    'org.openedx.learning.certificate.revoked.v1': {
        'learning-certificate-lifecycle':
            {'event_key_field': 'certificate.course.course_key', 'enabled': _should_send_certificate_events},
    },
    'org.openedx.learning.course.unenrollment.completed.v1': {
        'course-unenrollment-lifecycle':
            {'event_key_field': 'enrollment.course.course_key',
             # .. toggle_name: EVENT_BUS_PRODUCER_CONFIG['org.openedx.learning.course.unenrollment.completed.v1']
             #    ['course-unenrollment-lifecycle']['enabled']
             # .. toggle_implementation: DjangoSetting
             # .. toggle_default: False
             # .. toggle_description: Enables sending COURSE_UNENROLLMENT_COMPLETED events over the event bus.
             # .. toggle_use_cases: opt_in
             # .. toggle_creation_date: 2023-09-18
             # .. toggle_warning: The default may be changed in a later release. See
             #   https://github.com/openedx/openedx-events/issues/265
             # .. toggle_tickets: https://github.com/openedx/openedx-events/issues/210
             'enabled': False},
    },
    'org.openedx.learning.xblock.skill.verified.v1': {
        'learning-xblock-skill-verified':
            {'event_key_field': 'xblock_info.usage_key',
             # .. toggle_name: EVENT_BUS_PRODUCER_CONFIG['org.openedx.learning.xblock.skill.verified.v1']
             #    ['learning-xblock-skill-verified']['enabled']
             # .. toggle_implementation: DjangoSetting
             # .. toggle_default: False
             # .. toggle_description: Enables sending xblock_skill_verified events over the event bus.
             # .. toggle_use_cases: opt_in
             # .. toggle_creation_date: 2023-09-18
             # .. toggle_warning: The default may be changed in a later release. See
             #   https://github.com/openedx/openedx-events/issues/265
             # .. toggle_tickets: https://github.com/openedx/openedx-events/issues/210
             'enabled': False}
    },
    'org.openedx.learning.user.course_access_role.added.v1': {
        'learning-course-access-role-lifecycle':
            {'event_key_field': 'course_access_role_data.course_key', 'enabled': False},
    },
    'org.openedx.learning.user.course_access_role.removed.v1': {
        'learning-course-access-role-lifecycle':
            {'event_key_field': 'course_access_role_data.course_key', 'enabled': False},
    },
    # CMS events. These have to be copied over here because cms.common adds some derived entries as well,
    # and the derivation fails if the keys are missing. If we ever fully decouple the lms and cms settings,
    # we can remove these.
    'org.openedx.content_authoring.xblock.published.v1': {
        'course-authoring-xblock-lifecycle':
            {'event_key_field': 'xblock_info.usage_key', 'enabled': False},
    },
    'org.openedx.content_authoring.xblock.deleted.v1': {
        'course-authoring-xblock-lifecycle':
            {'event_key_field': 'xblock_info.usage_key', 'enabled': False},
    },
    'org.openedx.content_authoring.xblock.duplicated.v1': {
        'course-authoring-xblock-lifecycle':
            {'event_key_field': 'xblock_info.usage_key', 'enabled': False},
    },
    "org.openedx.learning.course.passing.status.updated.v1": {
        "learning-badges-lifecycle": {
            "event_key_field": "course_passing_status.course.course_key",
            "enabled": _should_send_learning_badge_events,
        },
    },
    "org.openedx.learning.ccx.course.passing.status.updated.v1": {
        "learning-badges-lifecycle": {
            "event_key_field": "course_passing_status.course.ccx_course_key",
            "enabled": _should_send_learning_badge_events,
        },
    },
}
derived_collection_entry('EVENT_BUS_PRODUCER_CONFIG', 'org.openedx.learning.certificate.created.v1',
                         'learning-certificate-lifecycle', 'enabled')
derived_collection_entry('EVENT_BUS_PRODUCER_CONFIG', 'org.openedx.learning.certificate.revoked.v1',
                         'learning-certificate-lifecycle', 'enabled')

derived_collection_entry(
    "EVENT_BUS_PRODUCER_CONFIG",
    "org.openedx.learning.course.passing.status.updated.v1",
    "learning-badges-lifecycle",
    "enabled",
)
derived_collection_entry(
    "EVENT_BUS_PRODUCER_CONFIG",
    "org.openedx.learning.ccx.course.passing.status.updated.v1",
    "learning-badges-lifecycle",
    "enabled",
)

BEAMER_PRODUCT_ID = ""

#### Survey Report ####
# .. toggle_name: SURVEY_REPORT_ENABLE
# .. toggle_implementation: DjangoSetting
# .. toggle_default: True
# .. toggle_description: Set to True to enable the feature to generate and send survey reports.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2024-01-30
SURVEY_REPORT_ENABLE = True
# .. setting_name: SURVEY_REPORT_ENDPOINT
# .. setting_default: Open edX organization endpoint
# .. setting_description: Endpoint where the report will be sent.
SURVEY_REPORT_ENDPOINT = 'https://hooks.zapier.com/hooks/catch/11595998/3ouwv7m/'
# .. toggle_name: ANONYMOUS_SURVEY_REPORT
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: If enable, the survey report will be send a UUID as ID instead of use lms site name.
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2023-02-21
ANONYMOUS_SURVEY_REPORT = False
# .. setting_name: SURVEY_REPORT_CHECK_THRESHOLD
# .. setting_default: every 6 months
# .. setting_description: Survey report banner will appear if a survey report is not sent in the months defined.
SURVEY_REPORT_CHECK_THRESHOLD = 6
# .. setting_name: SURVEY_REPORT_EXTRA_DATA
# .. setting_default: empty dictionary
# .. setting_description: Dictionary with additional information that you want to share in the report.
SURVEY_REPORT_EXTRA_DATA = {}
# @@@@@@@@@ LMS_CFG yaml
SITE_NAME = "local.edly.io"
BOOK_URL = ""
LOG_DIR = "/openedx/data/logs"
LOGGING_ENV = "sandbox"
OAUTH_OIDC_ISSUER = "http://local.edly.io/oauth2"
PLATFORM_NAME = "Kyle's Open edX"
FEATURES = {
    "CERTIFICATES_HTML_VIEW": true,
    "PREVIEW_LMS_BASE": "preview.local.edly.io",
    "ENABLE_COURSE_DISCOVERY": true,
    "ENABLE_COURSEWARE_SEARCH": true,
    "ENABLE_CSMH_EXTENDED": false,
    "ENABLE_DASHBOARD_SEARCH": true,
    "ENABLE_COMBINED_LOGIN_REGISTRATION": true,
    "ENABLE_GRADE_DOWNLOADS": true,
    "ENABLE_LEARNER_RECORDS": false,
    "ENABLE_MOBILE_REST_API": true,
    "ENABLE_OAUTH2_PROVIDER": true,
    "ENABLE_PREREQUISITE_COURSES": true,
    "ENABLE_THIRD_PARTY_AUTH": true,
    "MILESTONES_APP": true
}
LMS_ROOT_URL = "http://local.edly.io"
CMS_ROOT_URL = "http://studio.local.edly.io"
CMS_BASE = "studio.local.edly.io"
LMS_BASE = "local.edly.io"
CONTACT_EMAIL = "contact@local.overhang.io"
CELERY_BROKER_TRANSPORT = "redis"
CELERY_BROKER_HOSTNAME = "redis:6379"
CELERY_BROKER_VHOST = "0"
CELERY_BROKER_USER = ""
CELERY_BROKER_PASSWORD = ""
ALTERNATE_WORKER_QUEUES = "cms"
ENABLE_COMPREHENSIVE_THEMING = true
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp"
EMAIL_PORT = 8025
EMAIL_USE_TLS = false
ACE_ROUTING_KEY = "edx.lms.core.default"
HTTPS = "off"
LANGUAGE_CODE = "en"
SESSION_COOKIE_DOMAIN = "local.edly.io"
SECRET_KEY = "o5wToOrEitfAxwP8E5U0n5zi"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
DOC_STORE_CONFIG = null
XQUEUE_INTERFACE = {
    "django_auth": null,
    "url": null
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "mysql",
        "PORT": 3306,
        "NAME": "openedx",
        "USER": "openedx",
        "PASSWORD": "auLBXeYu",
        "ATOMIC_REQUESTS": true,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4"
        }
    }
}
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
# @@@@@@@@@ lms/envs/production.py
"""
This is the default template for our main set of AWS servers.

Common traits:
* Use memcached, and cache-backed sessions
* Use a MySQL 5.1 database
"""

# We intentionally define lots of variables that aren't used, and
# want to import all variables from base settings files
# pylint: disable=wildcard-import, unused-wildcard-import

# Pylint gets confused by path.py instances, which report themselves as class
# objects. As a result, pylint applies the wrong regex in validating names,
# and throws spurious errors. Therefore, we disable invalid-name checking.
# pylint: disable=invalid-name


import codecs
import copy
import datetime
import os

import yaml
import django
from django.core.exceptions import ImproperlyConfigured
from edx_django_utils.plugins import add_plugins
from openedx_events.event_bus import merge_producer_configs
from path import Path as path

from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType
from openedx.core.lib.derived import derive_settings
from openedx.core.lib.logsettings import get_logger_config
from xmodule.modulestore.modulestore_settings import convert_module_store_setting_if_needed  # lint-amnesty, pylint: disable=wrong-import-order



def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)  # lint-amnesty, pylint: disable=raise-missing-from

################################ ALWAYS THE SAME ##############################

DEBUG = False
DEFAULT_TEMPLATE_ENGINE['OPTIONS']['debug'] = False

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# IMPORTANT: With this enabled, the server must always be behind a proxy that
# strips the header HTTP_X_FORWARDED_PROTO from client requests. Otherwise,
# a user can fool our server into thinking it was an https connection.
# See
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# for other warnings.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
################################ END ALWAYS THE SAME ##############################

# A file path to a YAML file from which to load all the configuration for the edx platform


try:
    # A file path to a YAML file from which to load all the code revisions currently deployed
    REVISION_CONFIG_FILE = get_env_setting('REVISION_CFG')

    with codecs.open(REVISION_CONFIG_FILE, encoding='utf-8') as f:
        REVISION_CONFIG = yaml.safe_load(f)
except Exception:  # pylint: disable=broad-except
    REVISION_CONFIG = {}

# Do NOT calculate this dynamically at startup with git because it's *slow*.
EDX_PLATFORM_REVISION = REVISION_CONFIG.get('EDX_PLATFORM_REVISION', EDX_PLATFORM_REVISION)

###################################### CELERY  ################################

# Don't use a connection pool, since connections are dropped by ELB.
BROKER_POOL_LIMIT = 0
BROKER_CONNECTION_TIMEOUT = 1

# Allow env to configure celery result backend with default set to django-cache
CELERY_RESULT_BACKEND = ENV_TOKENS.get('CELERY_RESULT_BACKEND', 'django-cache')

# When the broker is behind an ELB, use a heartbeat to refresh the
# connection and to detect if it has been dropped.
BROKER_HEARTBEAT = ENV_TOKENS.get('BROKER_HEARTBEAT', 60.0)
BROKER_HEARTBEAT_CHECKRATE = ENV_TOKENS.get('BROKER_HEARTBEAT_CHECKRATE', 2)

# Each worker should only fetch one message at a time
CELERYD_PREFETCH_MULTIPLIER = 1

# STATIC_ROOT specifies the directory where static files are
# collected
STATIC_ROOT_BASE = ENV_TOKENS.get('STATIC_ROOT_BASE', None)
if STATIC_ROOT_BASE:
    STATIC_ROOT = path(STATIC_ROOT_BASE)
    WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = STATIC_ROOT / "webpack-stats.json"
    WEBPACK_LOADER['WORKERS']['STATS_FILE'] = STATIC_ROOT / "webpack-worker-stats.json"


# STATIC_URL_BASE specifies the base url to use for static files
STATIC_URL_BASE = ENV_TOKENS.get('STATIC_URL_BASE', None)
if STATIC_URL_BASE:
    STATIC_URL = STATIC_URL_BASE
    if not STATIC_URL.endswith("/"):
        STATIC_URL += "/"

# Allow overriding build profile used by RequireJS with one
# contained on a custom theme
REQUIRE_BUILD_PROFILE = ENV_TOKENS.get('REQUIRE_BUILD_PROFILE', REQUIRE_BUILD_PROFILE)

# The following variables use (or) instead of the default value inside (get). This is to enforce using the Lazy Text
# values when the variable is an empty string. Therefore, setting these variable as empty text in related
# json files will make the system reads their values from django translation files
PLATFORM_NAME = ENV_TOKENS.get('PLATFORM_NAME') or PLATFORM_NAME
PLATFORM_DESCRIPTION = ENV_TOKENS.get('PLATFORM_DESCRIPTION') or PLATFORM_DESCRIPTION

DATA_DIR = path(ENV_TOKENS.get('DATA_DIR', DATA_DIR))
CC_MERCHANT_NAME = ENV_TOKENS.get('CC_MERCHANT_NAME', PLATFORM_NAME)
EMAIL_FILE_PATH = ENV_TOKENS.get('EMAIL_FILE_PATH', DATA_DIR / "emails" / "lms")
EMAIL_HOST = ENV_TOKENS.get('EMAIL_HOST', 'localhost')  # django default is localhost
EMAIL_PORT = ENV_TOKENS.get('EMAIL_PORT', 25)  # django default is 25
EMAIL_USE_TLS = ENV_TOKENS.get('EMAIL_USE_TLS', False)  # django default is False
SITE_NAME = ENV_TOKENS.get('SITE_NAME', SITE_NAME)
SESSION_COOKIE_DOMAIN = ENV_TOKENS.get('SESSION_COOKIE_DOMAIN')
SESSION_COOKIE_HTTPONLY = ENV_TOKENS.get('SESSION_COOKIE_HTTPONLY', True)

DCS_SESSION_COOKIE_SAMESITE = ENV_TOKENS.get('DCS_SESSION_COOKIE_SAMESITE', DCS_SESSION_COOKIE_SAMESITE)
DCS_SESSION_COOKIE_SAMESITE_FORCE_ALL = ENV_TOKENS.get('DCS_SESSION_COOKIE_SAMESITE_FORCE_ALL', DCS_SESSION_COOKIE_SAMESITE_FORCE_ALL)  # lint-amnesty, pylint: disable=line-too-long

# As django-cookies-samesite package is set to be removed from base requirements when we upgrade to Django 3.2,
# we should follow the settings name provided by Django.
# https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-samesite
SESSION_COOKIE_SAMESITE = DCS_SESSION_COOKIE_SAMESITE

AWS_SES_REGION_NAME = ENV_TOKENS.get('AWS_SES_REGION_NAME', 'us-east-1')
AWS_SES_REGION_ENDPOINT = ENV_TOKENS.get('AWS_SES_REGION_ENDPOINT', 'email.us-east-1.amazonaws.com')

REGISTRATION_EMAIL_PATTERNS_ALLOWED = ENV_TOKENS.get('REGISTRATION_EMAIL_PATTERNS_ALLOWED')

LMS_ROOT_URL = ENV_TOKENS.get('LMS_ROOT_URL')
LMS_INTERNAL_ROOT_URL = ENV_TOKENS.get('LMS_INTERNAL_ROOT_URL', LMS_ROOT_URL)

# List of logout URIs for each IDA that the learner should be logged out of when they logout of the LMS. Only applies to
# IDA for which the social auth flow uses DOT (Django OAuth Toolkit).
IDA_LOGOUT_URI_LIST = ENV_TOKENS.get('IDA_LOGOUT_URI_LIST', [])

ENV_FEATURES = ENV_TOKENS.get('FEATURES', {})
for feature, value in ENV_FEATURES.items():
    FEATURES[feature] = value

CMS_BASE = ENV_TOKENS.get('CMS_BASE', 'studio.edx.org')

ALLOWED_HOSTS = [
    # TODO: bbeggs remove this before prod, temp fix to get load testing running
    "*",
    ENV_TOKENS.get('LMS_BASE'),
    FEATURES['PREVIEW_LMS_BASE'],
]

# Sometimes, OAuth2 clients want the user to redirect back to their site after logout. But to determine if the given
# redirect URL/path is safe for redirection, the following variable is used by edX.
LOGIN_REDIRECT_WHITELIST = ENV_TOKENS.get(
    'LOGIN_REDIRECT_WHITELIST',
    LOGIN_REDIRECT_WHITELIST
)

# allow for environments to specify what cookie name our login subsystem should use
# this is to fix a bug regarding simultaneous logins between edx.org and edge.edx.org which can
# happen with some browsers (e.g. Firefox)
if ENV_TOKENS.get('SESSION_COOKIE_NAME', None):
    # NOTE, there's a bug in Django (http://bugs.python.org/issue18012) which necessitates this being a str()
    SESSION_COOKIE_NAME = str(ENV_TOKENS.get('SESSION_COOKIE_NAME'))

# This is the domain that is used to set shared cookies between various sub-domains.
# By default, it's set to the same thing as the SESSION_COOKIE_DOMAIN, but we want to make it overrideable.
SHARED_COOKIE_DOMAIN = ENV_TOKENS.get('SHARED_COOKIE_DOMAIN', SESSION_COOKIE_DOMAIN)

CACHES = ENV_TOKENS.get('CACHES', CACHES)
# Cache used for location mapping -- called many times with the same key/value
# in a given request.
if 'loc_cache' not in CACHES:
    CACHES['loc_cache'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'edx_location_mem_cache',
    }

if 'staticfiles' in CACHES:
    CACHES['staticfiles']['KEY_PREFIX'] = EDX_PLATFORM_REVISION

# In order to transition from local disk asset storage to S3 backed asset storage,
# we need to run asset collection twice, once for local disk and once for S3.
# Once we have migrated to service assets off S3, then we can convert this back to
# managed by the yaml file contents
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', ENV_TOKENS.get('STATICFILES_STORAGE', STATICFILES_STORAGE))

# Load all AWS_ prefixed variables to allow an S3Boto3Storage to be configured
_locals = locals()
for key, value in ENV_TOKENS.items():
    if key.startswith('AWS_'):
        _locals[key] = value

# Currency
PAID_COURSE_REGISTRATION_CURRENCY = ENV_TOKENS.get('PAID_COURSE_REGISTRATION_CURRENCY',
                                                   PAID_COURSE_REGISTRATION_CURRENCY)

# We want Bulk Email running on the high-priority queue, so we define the
# routing key that points to it. At the moment, the name is the same.
# We have to reset the value here, since we have changed the value of the queue name.
BULK_EMAIL_ROUTING_KEY = ENV_TOKENS.get('BULK_EMAIL_ROUTING_KEY', HIGH_PRIORITY_QUEUE)

# We can run smaller jobs on the low priority queue. See note above for why
# we have to reset the value here.
BULK_EMAIL_ROUTING_KEY_SMALL_JOBS = ENV_TOKENS.get('BULK_EMAIL_ROUTING_KEY_SMALL_JOBS', DEFAULT_PRIORITY_QUEUE)

# Queue to use for expiring old entitlements
ENTITLEMENTS_EXPIRATION_ROUTING_KEY = ENV_TOKENS.get('ENTITLEMENTS_EXPIRATION_ROUTING_KEY', DEFAULT_PRIORITY_QUEUE)

# Message expiry time in seconds
CELERY_EVENT_QUEUE_TTL = ENV_TOKENS.get('CELERY_EVENT_QUEUE_TTL', None)

# Allow CELERY_QUEUES to be overwritten by ENV_TOKENS,
ENV_CELERY_QUEUES = ENV_TOKENS.get('CELERY_QUEUES', None)
if ENV_CELERY_QUEUES:
    CELERY_QUEUES = {queue: {} for queue in ENV_CELERY_QUEUES}

# Then add alternate environment queues
ALTERNATE_QUEUE_ENVS = ENV_TOKENS.get('ALTERNATE_WORKER_QUEUES', '').split()
ALTERNATE_QUEUES = [
    DEFAULT_PRIORITY_QUEUE.replace(QUEUE_VARIANT, alternate + '.')
    for alternate in ALTERNATE_QUEUE_ENVS
]
CELERY_QUEUES.update(
    {
        alternate: {}
        for alternate in ALTERNATE_QUEUES
        if alternate not in list(CELERY_QUEUES.keys())
    }
)

# following setting is for backward compatibility
if ENV_TOKENS.get('COMPREHENSIVE_THEME_DIR', None):
    COMPREHENSIVE_THEME_DIR = ENV_TOKENS.get('COMPREHENSIVE_THEME_DIR')


# COMPREHENSIVE_THEME_LOCALE_PATHS contain the paths to themes locale directories e.g.
# "COMPREHENSIVE_THEME_LOCALE_PATHS" : [
#        "/edx/src/edx-themes/conf/locale"
#    ],
COMPREHENSIVE_THEME_LOCALE_PATHS = ENV_TOKENS.get('COMPREHENSIVE_THEME_LOCALE_PATHS', [])


# PREPEND_LOCALE_PATHS contain the paths to locale directories to load first e.g.
# "PREPEND_LOCALE_PATHS" : [
#        "/edx/my-locale"
#    ],
PREPEND_LOCALE_PATHS = ENV_TOKENS.get('PREPEND_LOCALE_PATHS', [])


MKTG_URL_LINK_MAP.update(ENV_TOKENS.get('MKTG_URL_LINK_MAP', {}))
ENTERPRISE_MARKETING_FOOTER_QUERY_PARAMS = ENV_TOKENS.get(
    'ENTERPRISE_MARKETING_FOOTER_QUERY_PARAMS',
    ENTERPRISE_MARKETING_FOOTER_QUERY_PARAMS
)
# Marketing link overrides
MKTG_URL_OVERRIDES.update(ENV_TOKENS.get('MKTG_URL_OVERRIDES', MKTG_URL_OVERRIDES))

# Intentional defaults.
ID_VERIFICATION_SUPPORT_LINK = ENV_TOKENS.get('ID_VERIFICATION_SUPPORT_LINK', SUPPORT_SITE_LINK)
PASSWORD_RESET_SUPPORT_LINK = ENV_TOKENS.get('PASSWORD_RESET_SUPPORT_LINK', SUPPORT_SITE_LINK)
ACTIVATION_EMAIL_SUPPORT_LINK = ENV_TOKENS.get('ACTIVATION_EMAIL_SUPPORT_LINK', SUPPORT_SITE_LINK)
LOGIN_ISSUE_SUPPORT_LINK = ENV_TOKENS.get('LOGIN_ISSUE_SUPPORT_LINK', SUPPORT_SITE_LINK)

# Timezone overrides
TIME_ZONE = ENV_TOKENS.get('CELERY_TIMEZONE', CELERY_TIMEZONE)

# Translation overrides
LANGUAGE_DICT = dict(LANGUAGES)

LANGUAGE_COOKIE_NAME = ENV_TOKENS.get('LANGUAGE_COOKIE', None) or ENV_TOKENS.get(
    'LANGUAGE_COOKIE_NAME', LANGUAGE_COOKIE_NAME)

# Additional installed apps
for app in ENV_TOKENS.get('ADDL_INSTALLED_APPS', []):
    INSTALLED_APPS.append(app)


local_loglevel = ENV_TOKENS.get('LOCAL_LOGLEVEL', 'INFO')
LOG_DIR = ENV_TOKENS.get('LOG_DIR', LOG_DIR)

LOGGING = get_logger_config(LOG_DIR,
                            logging_env=ENV_TOKENS.get('LOGGING_ENV', LOGGING_ENV),
                            local_loglevel=local_loglevel,
                            service_variant=SERVICE_VARIANT)

COURSE_LISTINGS = ENV_TOKENS.get('COURSE_LISTINGS', {})
COMMENTS_SERVICE_URL = ENV_TOKENS.get("COMMENTS_SERVICE_URL", '')
COMMENTS_SERVICE_KEY = ENV_TOKENS.get("COMMENTS_SERVICE_KEY", '')
CERT_QUEUE = ENV_TOKENS.get("CERT_QUEUE", 'test-pull')

# Python lib settings
PYTHON_LIB_FILENAME = ENV_TOKENS.get('PYTHON_LIB_FILENAME', 'python_lib.zip')

# Code jail settings
for name, value in ENV_TOKENS.get("CODE_JAIL", {}).items():
    oldvalue = CODE_JAIL.get(name)
    if isinstance(oldvalue, dict):
        for subname, subvalue in value.items():
            oldvalue[subname] = subvalue
    else:
        CODE_JAIL[name] = value

COURSES_WITH_UNSAFE_CODE = ENV_TOKENS.get("COURSES_WITH_UNSAFE_CODE", [])

# Event Tracking
if "TRACKING_IGNORE_URL_PATTERNS" in ENV_TOKENS:
    TRACKING_IGNORE_URL_PATTERNS = ENV_TOKENS.get("TRACKING_IGNORE_URL_PATTERNS")

# SSL external authentication settings
SSL_AUTH_EMAIL_DOMAIN = ENV_TOKENS.get("SSL_AUTH_EMAIL_DOMAIN", "MIT.EDU")
SSL_AUTH_DN_FORMAT_STRING = ENV_TOKENS.get(
    "SSL_AUTH_DN_FORMAT_STRING",
    "/C=US/ST=Massachusetts/O=Massachusetts Institute of Technology/OU=Client CA v1/CN={0}/emailAddress={1}"
)

# Video Caching. Pairing country codes with CDN URLs.
# Example: {'CN': 'http://api.xuetangx.com/edx/video?s3_url='}
VIDEO_CDN_URL = ENV_TOKENS.get('VIDEO_CDN_URL', {})

# Determines whether the CSRF token can be transported on
# unencrypted channels. It is set to False here for backward compatibility,
# but it is highly recommended that this is True for environments accessed
# by end users.
CSRF_COOKIE_SECURE = ENV_TOKENS.get('CSRF_COOKIE_SECURE', False)

# Determines which origins are trusted for unsafe requests eg. POST requests.
CSRF_TRUSTED_ORIGINS = ENV_TOKENS.get('CSRF_TRUSTED_ORIGINS', [])
# values are already updated above with default CSRF_TRUSTED_ORIGINS values but in
# case of new django version these values will override.
if django.VERSION[0] >= 4:  # for greater than django 3.2 use schemes.
    CSRF_TRUSTED_ORIGINS = ENV_TOKENS.get('CSRF_TRUSTED_ORIGINS_WITH_SCHEME', [])

############# CORS headers for cross-domain requests #################

if FEATURES.get('ENABLE_CORS_HEADERS') or FEATURES.get('ENABLE_CROSS_DOMAIN_CSRF_COOKIE'):
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = ENV_TOKENS.get('CORS_ORIGIN_WHITELIST', ())

    CORS_ORIGIN_ALLOW_ALL = ENV_TOKENS.get('CORS_ORIGIN_ALLOW_ALL', False)
    CORS_ALLOW_INSECURE = ENV_TOKENS.get('CORS_ALLOW_INSECURE', False)

    # If setting a cross-domain cookie, it's really important to choose
    # a name for the cookie that is DIFFERENT than the cookies used
    # by each subdomain.  For example, suppose the applications
    # at these subdomains are configured to use the following cookie names:
    #
    # 1) foo.example.com --> "csrftoken"
    # 2) baz.example.com --> "csrftoken"
    # 3) bar.example.com --> "csrftoken"
    #
    # For the cross-domain version of the CSRF cookie, you need to choose
    # a name DIFFERENT than "csrftoken"; otherwise, the new token configured
    # for ".example.com" could conflict with the other cookies,
    # non-deterministically causing 403 responses.
    #
    # Because of the way Django stores cookies, the cookie name MUST
    # be a `str`, not unicode.  Otherwise there will `TypeError`s will be raised
    # when Django tries to call the unicode `translate()` method with the wrong
    # number of parameters.
    CROSS_DOMAIN_CSRF_COOKIE_NAME = str(ENV_TOKENS.get('CROSS_DOMAIN_CSRF_COOKIE_NAME'))

    # When setting the domain for the "cross-domain" version of the CSRF
    # cookie, you should choose something like: ".example.com"
    # (note the leading dot), where both the referer and the host
    # are subdomains of "example.com".
    #
    # Browser security rules require that
    # the cookie domain matches the domain of the server; otherwise
    # the cookie won't get set.  And once the cookie gets set, the client
    # needs to be on a domain that matches the cookie domain, otherwise
    # the client won't be able to read the cookie.
    CROSS_DOMAIN_CSRF_COOKIE_DOMAIN = ENV_TOKENS.get('CROSS_DOMAIN_CSRF_COOKIE_DOMAIN')


# Field overrides. To use the IDDE feature, add
# 'courseware.student_field_overrides.IndividualStudentOverrideProvider'.
FIELD_OVERRIDE_PROVIDERS = tuple(ENV_TOKENS.get('FIELD_OVERRIDE_PROVIDERS', []))

############### XBlock filesystem field config ##########
if 'DJFS' in AUTH_TOKENS and AUTH_TOKENS['DJFS'] is not None:
    DJFS = AUTH_TOKENS['DJFS']

############### Module Store Items ##########
HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS = ENV_TOKENS.get('HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS', {})
# PREVIEW DOMAIN must be present in HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS for the preview to show draft changes
if 'PREVIEW_LMS_BASE' in FEATURES and FEATURES['PREVIEW_LMS_BASE'] != '':
    PREVIEW_DOMAIN = FEATURES['PREVIEW_LMS_BASE'].split(':')[0]
    # update dictionary with preview domain regex
    HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS.update({
        PREVIEW_DOMAIN: 'draft-preferred'
    })

MODULESTORE_FIELD_OVERRIDE_PROVIDERS = ENV_TOKENS.get(
    'MODULESTORE_FIELD_OVERRIDE_PROVIDERS',
    MODULESTORE_FIELD_OVERRIDE_PROVIDERS
)

XBLOCK_FIELD_DATA_WRAPPERS = ENV_TOKENS.get(
    'XBLOCK_FIELD_DATA_WRAPPERS',
    XBLOCK_FIELD_DATA_WRAPPERS
)

############### Mixed Related(Secure/Not-Secure) Items ##########
LMS_SEGMENT_KEY = AUTH_TOKENS.get('SEGMENT_KEY')

SECRET_KEY = AUTH_TOKENS['SECRET_KEY']

AWS_ACCESS_KEY_ID = AUTH_TOKENS.get("AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID)
if AWS_ACCESS_KEY_ID == "":
    AWS_ACCESS_KEY_ID = None

AWS_SECRET_ACCESS_KEY = AUTH_TOKENS.get("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)
if AWS_SECRET_ACCESS_KEY == "":
    AWS_SECRET_ACCESS_KEY = None

# these variable already exists in cms with `private` value. django-storages starting `1.10.1`
# does not set acl values till 1.9.1 default-acl is `public-read`. To maintain the behaviour
# same with upcoming version setting it to `public-read`.
AWS_DEFAULT_ACL = 'public-read'
AWS_BUCKET_ACL = AWS_DEFAULT_ACL
AWS_STORAGE_BUCKET_NAME = AUTH_TOKENS.get('AWS_STORAGE_BUCKET_NAME', 'edxuploads')

# Disabling querystring auth instructs Boto to exclude the querystring parameters (e.g. signature, access key) it
# normally appends to every returned URL.
AWS_QUERYSTRING_AUTH = AUTH_TOKENS.get('AWS_QUERYSTRING_AUTH', True)
AWS_S3_CUSTOM_DOMAIN = AUTH_TOKENS.get('AWS_S3_CUSTOM_DOMAIN', 'edxuploads.s3.amazonaws.com')

if AUTH_TOKENS.get('DEFAULT_FILE_STORAGE'):
    DEFAULT_FILE_STORAGE = AUTH_TOKENS.get('DEFAULT_FILE_STORAGE')
elif AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# If there is a database called 'read_replica', you can use the use_read_replica_if_available
# function in util/query.py, which is useful for very large database reads
DATABASES = AUTH_TOKENS.get('DATABASES', DATABASES)

# The normal database user does not have enough permissions to run migrations.
# Migrations are run with separate credentials, given as DB_MIGRATION_*
# environment variables
for name, database in DATABASES.items():
    if name != 'read_replica':
        database.update({
            'ENGINE': os.environ.get('DB_MIGRATION_ENGINE', database['ENGINE']),
            'USER': os.environ.get('DB_MIGRATION_USER', database['USER']),
            'PASSWORD': os.environ.get('DB_MIGRATION_PASS', database['PASSWORD']),
            'NAME': os.environ.get('DB_MIGRATION_NAME', database['NAME']),
            'HOST': os.environ.get('DB_MIGRATION_HOST', database['HOST']),
            'PORT': os.environ.get('DB_MIGRATION_PORT', database['PORT']),
        })

XQUEUE_INTERFACE = AUTH_TOKENS.get('XQUEUE_INTERFACE', XQUEUE_INTERFACE)

# Get the MODULESTORE from auth.json, but if it doesn't exist,
# use the one from common.py
MODULESTORE = convert_module_store_setting_if_needed(AUTH_TOKENS.get('MODULESTORE', MODULESTORE))

# After conversion above, the modulestore will have a "stores" list with all defined stores, for all stores, add the
# fs_root entry to derived collection so that if it's a callable it can be resolved.  We need to do this because the
# `derived_collection_entry` takes an exact index value but the config file might have overridden the number of stores
# and so we can't be sure that the 2 we define in common.py will be there when we try to derive settings.  This could
# lead to exceptions being thrown when the `derive_settings` call later in this file tries to update settings.  We call
# the derived_collection_entry function here to ensure that we update the fs_root for any callables that remain after
# we've updated the MODULESTORE setting from our config file.
for idx, store in enumerate(MODULESTORE['default']['OPTIONS']['stores']):
    if 'OPTIONS' in store and 'fs_root' in store["OPTIONS"]:
        derived_collection_entry('MODULESTORE', 'default', 'OPTIONS', 'stores', idx, 'OPTIONS', 'fs_root')

MONGODB_LOG = AUTH_TOKENS.get('MONGODB_LOG', {})

EMAIL_HOST_USER = AUTH_TOKENS.get('EMAIL_HOST_USER', '')  # django default is ''
EMAIL_HOST_PASSWORD = AUTH_TOKENS.get('EMAIL_HOST_PASSWORD', '')  # django default is ''

# Analytics API
ANALYTICS_API_KEY = AUTH_TOKENS.get("ANALYTICS_API_KEY", ANALYTICS_API_KEY)
ANALYTICS_API_URL = ENV_TOKENS.get("ANALYTICS_API_URL", ANALYTICS_API_URL)

# Zendesk
ZENDESK_USER = AUTH_TOKENS.get("ZENDESK_USER")
ZENDESK_API_KEY = AUTH_TOKENS.get("ZENDESK_API_KEY")

# API Key for inbound requests from Notifier service
EDX_API_KEY = AUTH_TOKENS.get("EDX_API_KEY")

# Celery Broker
CELERY_BROKER_TRANSPORT = ENV_TOKENS.get("CELERY_BROKER_TRANSPORT", "")
CELERY_BROKER_HOSTNAME = ENV_TOKENS.get("CELERY_BROKER_HOSTNAME", "")
CELERY_BROKER_VHOST = ENV_TOKENS.get("CELERY_BROKER_VHOST", "")
CELERY_BROKER_USER = AUTH_TOKENS.get("CELERY_BROKER_USER", "")
CELERY_BROKER_PASSWORD = AUTH_TOKENS.get("CELERY_BROKER_PASSWORD", "")

BROKER_URL = "{}://{}:{}@{}/{}".format(CELERY_BROKER_TRANSPORT,
                                       CELERY_BROKER_USER,
                                       CELERY_BROKER_PASSWORD,
                                       CELERY_BROKER_HOSTNAME,
                                       CELERY_BROKER_VHOST)
BROKER_USE_SSL = ENV_TOKENS.get('CELERY_BROKER_USE_SSL', False)

try:
    BROKER_TRANSPORT_OPTIONS = {
        'fanout_patterns': True,
        'fanout_prefix': True,
        **ENV_TOKENS.get('CELERY_BROKER_TRANSPORT_OPTIONS', {})
    }
except TypeError as exc:
    raise ImproperlyConfigured('CELERY_BROKER_TRANSPORT_OPTIONS must be a dict') from exc

# Block Structures

# upload limits
STUDENT_FILEUPLOAD_MAX_SIZE = ENV_TOKENS.get("STUDENT_FILEUPLOAD_MAX_SIZE", STUDENT_FILEUPLOAD_MAX_SIZE)

# Event tracking
TRACKING_BACKENDS.update(AUTH_TOKENS.get("TRACKING_BACKENDS", {}))
EVENT_TRACKING_BACKENDS['tracking_logs']['OPTIONS']['backends'].update(AUTH_TOKENS.get("EVENT_TRACKING_BACKENDS", {}))
EVENT_TRACKING_BACKENDS['segmentio']['OPTIONS']['processors'][0]['OPTIONS']['whitelist'].extend(
    AUTH_TOKENS.get("EVENT_TRACKING_SEGMENTIO_EMIT_WHITELIST", []))
TRACKING_SEGMENTIO_WEBHOOK_SECRET = AUTH_TOKENS.get(
    "TRACKING_SEGMENTIO_WEBHOOK_SECRET",
    TRACKING_SEGMENTIO_WEBHOOK_SECRET
)
TRACKING_SEGMENTIO_ALLOWED_TYPES = ENV_TOKENS.get("TRACKING_SEGMENTIO_ALLOWED_TYPES", TRACKING_SEGMENTIO_ALLOWED_TYPES)
TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES = ENV_TOKENS.get(
    "TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES",
    TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES
)
TRACKING_SEGMENTIO_SOURCE_MAP = ENV_TOKENS.get("TRACKING_SEGMENTIO_SOURCE_MAP", TRACKING_SEGMENTIO_SOURCE_MAP)

# Heartbeat
HEARTBEAT_CELERY_ROUTING_KEY = ENV_TOKENS.get('HEARTBEAT_CELERY_ROUTING_KEY', HEARTBEAT_CELERY_ROUTING_KEY)

# Student identity verification settings
VERIFY_STUDENT = AUTH_TOKENS.get("VERIFY_STUDENT", VERIFY_STUDENT)
DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH = ENV_TOKENS.get(
    "DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH",
    DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH
)

# Grades download
GRADES_DOWNLOAD_ROUTING_KEY = ENV_TOKENS.get('GRADES_DOWNLOAD_ROUTING_KEY', HIGH_MEM_QUEUE)

GRADES_DOWNLOAD = ENV_TOKENS.get("GRADES_DOWNLOAD", GRADES_DOWNLOAD)

# Rate limit for regrading tasks that a grading policy change can kick off

# financial reports
FINANCIAL_REPORTS = ENV_TOKENS.get("FINANCIAL_REPORTS", FINANCIAL_REPORTS)

##### ORA2 ######
# Prefix for uploads of example-based assessment AI classifiers
# This can be used to separate uploads for different environments
# within the same S3 bucket.
ORA2_FILE_PREFIX = ENV_TOKENS.get("ORA2_FILE_PREFIX", ORA2_FILE_PREFIX)

##### ACCOUNT LOCKOUT DEFAULT PARAMETERS #####
MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED = ENV_TOKENS.get(
    "MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED", MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED
)

MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS = ENV_TOKENS.get(
    "MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS", MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS
)

##### LOGISTRATION RATE LIMIT SETTINGS #####
LOGISTRATION_RATELIMIT_RATE = ENV_TOKENS.get('LOGISTRATION_RATELIMIT_RATE', LOGISTRATION_RATELIMIT_RATE)
LOGISTRATION_API_RATELIMIT = ENV_TOKENS.get('LOGISTRATION_API_RATELIMIT', LOGISTRATION_API_RATELIMIT)
LOGIN_AND_REGISTER_FORM_RATELIMIT = ENV_TOKENS.get(
    'LOGIN_AND_REGISTER_FORM_RATELIMIT', LOGIN_AND_REGISTER_FORM_RATELIMIT
)
RESET_PASSWORD_TOKEN_VALIDATE_API_RATELIMIT = ENV_TOKENS.get(
    'RESET_PASSWORD_TOKEN_VALIDATE_API_RATELIMIT', RESET_PASSWORD_TOKEN_VALIDATE_API_RATELIMIT
)
RESET_PASSWORD_API_RATELIMIT = ENV_TOKENS.get('RESET_PASSWORD_API_RATELIMIT', RESET_PASSWORD_API_RATELIMIT)

##### REGISTRATION RATE LIMIT SETTINGS #####
REGISTRATION_VALIDATION_RATELIMIT = ENV_TOKENS.get(
    'REGISTRATION_VALIDATION_RATELIMIT', REGISTRATION_VALIDATION_RATELIMIT
)

REGISTRATION_RATELIMIT = ENV_TOKENS.get('REGISTRATION_RATELIMIT', REGISTRATION_RATELIMIT)

#### PASSWORD POLICY SETTINGS #####
AUTH_PASSWORD_VALIDATORS = ENV_TOKENS.get("AUTH_PASSWORD_VALIDATORS", AUTH_PASSWORD_VALIDATORS)

### INACTIVITY SETTINGS ####
SESSION_INACTIVITY_TIMEOUT_IN_SECONDS = AUTH_TOKENS.get("SESSION_INACTIVITY_TIMEOUT_IN_SECONDS")

##### LMS DEADLINE DISPLAY TIME_ZONE #######
TIME_ZONE_DISPLAYED_FOR_DEADLINES = ENV_TOKENS.get("TIME_ZONE_DISPLAYED_FOR_DEADLINES",
                                                   TIME_ZONE_DISPLAYED_FOR_DEADLINES)

#### PROCTORED EXAM SETTINGS ####
PROCTORED_EXAM_VIEWABLE_PAST_DUE = ENV_TOKENS.get('PROCTORED_EXAM_VIEWABLE_PAST_DUE', False)

##### Third-party auth options ################################################
ENABLE_REQUIRE_THIRD_PARTY_AUTH = ENV_TOKENS.get('ENABLE_REQUIRE_THIRD_PARTY_AUTH', False)

if FEATURES.get('ENABLE_THIRD_PARTY_AUTH'):
    tmp_backends = ENV_TOKENS.get('THIRD_PARTY_AUTH_BACKENDS', [
        'social_core.backends.google.GoogleOAuth2',
        'social_core.backends.linkedin.LinkedinOAuth2',
        'social_core.backends.facebook.FacebookOAuth2',
        'social_core.backends.azuread.AzureADOAuth2',
        'common.djangoapps.third_party_auth.appleid.AppleIdAuth',  # vendored 'social_core.backends.apple.AppleIdAuth'
        'common.djangoapps.third_party_auth.identityserver3.IdentityServer3',
        'common.djangoapps.third_party_auth.saml.SAMLAuthBackend',
        'common.djangoapps.third_party_auth.lti.LTIAuthBackend',
    ])

    AUTHENTICATION_BACKENDS = list(tmp_backends) + list(AUTHENTICATION_BACKENDS)
    del tmp_backends

    # The reduced session expiry time during the third party login pipeline. (Value in seconds)
    SOCIAL_AUTH_PIPELINE_TIMEOUT = ENV_TOKENS.get('SOCIAL_AUTH_PIPELINE_TIMEOUT', 600)

    # Most provider configuration is done via ConfigurationModels but for a few sensitive values
    # we allow configuration via AUTH_TOKENS instead (optionally).
    # The SAML private/public key values do not need the delimiter lines (such as
    # "-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----" etc.) but they may be included
    # if you want (though it's easier to format the key values as JSON without the delimiters).
    SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = AUTH_TOKENS.get('SOCIAL_AUTH_SAML_SP_PRIVATE_KEY', '')
    SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = AUTH_TOKENS.get('SOCIAL_AUTH_SAML_SP_PUBLIC_CERT', '')
    SOCIAL_AUTH_SAML_SP_PRIVATE_KEY_DICT = AUTH_TOKENS.get('SOCIAL_AUTH_SAML_SP_PRIVATE_KEY_DICT', {})
    SOCIAL_AUTH_SAML_SP_PUBLIC_CERT_DICT = AUTH_TOKENS.get('SOCIAL_AUTH_SAML_SP_PUBLIC_CERT_DICT', {})
    SOCIAL_AUTH_OAUTH_SECRETS = AUTH_TOKENS.get('SOCIAL_AUTH_OAUTH_SECRETS', {})
    SOCIAL_AUTH_LTI_CONSUMER_SECRETS = AUTH_TOKENS.get('SOCIAL_AUTH_LTI_CONSUMER_SECRETS', {})

    # third_party_auth config moved to ConfigurationModels. This is for data migration only:
    THIRD_PARTY_AUTH_OLD_CONFIG = AUTH_TOKENS.get('THIRD_PARTY_AUTH', None)

    if ENV_TOKENS.get('THIRD_PARTY_AUTH_SAML_FETCH_PERIOD_HOURS', 24) is not None:
        CELERYBEAT_SCHEDULE['refresh-saml-metadata'] = {
            'task': 'common.djangoapps.third_party_auth.fetch_saml_metadata',
            'schedule': datetime.timedelta(hours=ENV_TOKENS.get('THIRD_PARTY_AUTH_SAML_FETCH_PERIOD_HOURS', 24)),
        }

    # The following can be used to integrate a custom login form with third_party_auth.
    # It should be a dict where the key is a word passed via ?auth_entry=, and the value is a
    # dict with an arbitrary 'secret_key' and a 'url'.
    THIRD_PARTY_AUTH_CUSTOM_AUTH_FORMS = AUTH_TOKENS.get('THIRD_PARTY_AUTH_CUSTOM_AUTH_FORMS', {})

##### OAUTH2 Provider ##############
if FEATURES.get('ENABLE_OAUTH2_PROVIDER'):
    OAUTH_ENFORCE_SECURE = ENV_TOKENS.get('OAUTH_ENFORCE_SECURE', True)
    OAUTH_ENFORCE_CLIENT_SECURE = ENV_TOKENS.get('OAUTH_ENFORCE_CLIENT_SECURE', True)
    # Defaults for the following are defined in lms.envs.common
    OAUTH_EXPIRE_DELTA = datetime.timedelta(
        days=ENV_TOKENS.get('OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS', OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS)
    )
    OAUTH_EXPIRE_DELTA_PUBLIC = datetime.timedelta(
        days=ENV_TOKENS.get('OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS', OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS)
    )


##### GOOGLE ANALYTICS IDS #####
GOOGLE_ANALYTICS_ACCOUNT = AUTH_TOKENS.get('GOOGLE_ANALYTICS_ACCOUNT')
GOOGLE_ANALYTICS_TRACKING_ID = AUTH_TOKENS.get('GOOGLE_ANALYTICS_TRACKING_ID')
GOOGLE_ANALYTICS_LINKEDIN = AUTH_TOKENS.get('GOOGLE_ANALYTICS_LINKEDIN')
GOOGLE_SITE_VERIFICATION_ID = ENV_TOKENS.get('GOOGLE_SITE_VERIFICATION_ID')
GOOGLE_ANALYTICS_4_ID = AUTH_TOKENS.get('GOOGLE_ANALYTICS_4_ID')

##### BRANCH.IO KEY #####
BRANCH_IO_KEY = AUTH_TOKENS.get('BRANCH_IO_KEY')

#### Course Registration Code length ####
REGISTRATION_CODE_LENGTH = ENV_TOKENS.get('REGISTRATION_CODE_LENGTH', 8)

# Which access.py permission names to check;
# We default this to the legacy permission 'see_exists'.
COURSE_CATALOG_VISIBILITY_PERMISSION = ENV_TOKENS.get(
    'COURSE_CATALOG_VISIBILITY_PERMISSION',
    COURSE_CATALOG_VISIBILITY_PERMISSION
)
COURSE_ABOUT_VISIBILITY_PERMISSION = ENV_TOKENS.get(
    'COURSE_ABOUT_VISIBILITY_PERMISSION',
    COURSE_ABOUT_VISIBILITY_PERMISSION
)

DEFAULT_COURSE_VISIBILITY_IN_CATALOG = ENV_TOKENS.get(
    'DEFAULT_COURSE_VISIBILITY_IN_CATALOG',
    DEFAULT_COURSE_VISIBILITY_IN_CATALOG
)

DEFAULT_MOBILE_AVAILABLE = ENV_TOKENS.get(
    'DEFAULT_MOBILE_AVAILABLE',
    DEFAULT_MOBILE_AVAILABLE
)

# Enrollment API Cache Timeout
ENROLLMENT_COURSE_DETAILS_CACHE_TIMEOUT = ENV_TOKENS.get('ENROLLMENT_COURSE_DETAILS_CACHE_TIMEOUT', 60)

# Ecommerce Orders API Cache Timeout
ECOMMERCE_ORDERS_API_CACHE_TIMEOUT = ENV_TOKENS.get('ECOMMERCE_ORDERS_API_CACHE_TIMEOUT', 3600)

if FEATURES.get('ENABLE_COURSEWARE_SEARCH') or \
   FEATURES.get('ENABLE_DASHBOARD_SEARCH') or \
   FEATURES.get('ENABLE_COURSE_DISCOVERY') or \
   FEATURES.get('ENABLE_TEAMS'):
    # Use ElasticSearch as the search engine herein
    SEARCH_ENGINE = "search.elastic.ElasticSearchEngine"
    SEARCH_FILTER_GENERATOR = ENV_TOKENS.get('SEARCH_FILTER_GENERATOR', SEARCH_FILTER_GENERATOR)

SEARCH_SKIP_INVITATION_ONLY_FILTERING = ENV_TOKENS.get(
    'SEARCH_SKIP_INVITATION_ONLY_FILTERING',
    SEARCH_SKIP_INVITATION_ONLY_FILTERING,
)
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = ENV_TOKENS.get(
    'SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING',
    SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING,
)

SEARCH_COURSEWARE_CONTENT_LOG_PARAMS = ENV_TOKENS.get(
    'SEARCH_COURSEWARE_CONTENT_LOG_PARAMS',
    SEARCH_COURSEWARE_CONTENT_LOG_PARAMS,
)

# TODO: Once we have successfully upgraded to ES7, switch this back to ELASTIC_SEARCH_CONFIG.
ELASTIC_SEARCH_CONFIG = ENV_TOKENS.get('ELASTIC_SEARCH_CONFIG_ES7', [{}])

# Facebook app
FACEBOOK_API_VERSION = AUTH_TOKENS.get("FACEBOOK_API_VERSION")
FACEBOOK_APP_SECRET = AUTH_TOKENS.get("FACEBOOK_APP_SECRET")
FACEBOOK_APP_ID = AUTH_TOKENS.get("FACEBOOK_APP_ID")

XBLOCK_SETTINGS = ENV_TOKENS.get('XBLOCK_SETTINGS', {})
XBLOCK_SETTINGS.setdefault("VideoBlock", {})["licensing_enabled"] = FEATURES.get("LICENSING", False)
XBLOCK_SETTINGS.setdefault("VideoBlock", {})['YOUTUBE_API_KEY'] = AUTH_TOKENS.get('YOUTUBE_API_KEY', YOUTUBE_API_KEY)

##### Custom Courses for EdX #####
if FEATURES.get('CUSTOM_COURSES_EDX'):
    INSTALLED_APPS += ['lms.djangoapps.ccx', 'openedx.core.djangoapps.ccxcon.apps.CCXConnectorConfig']
    MODULESTORE_FIELD_OVERRIDE_PROVIDERS += (
        'lms.djangoapps.ccx.overrides.CustomCoursesForEdxOverrideProvider',
    )

##### Individual Due Date Extensions #####
if FEATURES.get('INDIVIDUAL_DUE_DATES'):
    FIELD_OVERRIDE_PROVIDERS += (
        'lms.djangoapps.courseware.student_field_overrides.IndividualStudentOverrideProvider',
    )

##### Show Answer Override for Self-Paced Courses #####
FIELD_OVERRIDE_PROVIDERS += (
    'openedx.features.personalized_learner_schedules.show_answer.show_answer_field_override.ShowAnswerFieldOverride',
)

##### Self-Paced Course Due Dates #####
XBLOCK_FIELD_DATA_WRAPPERS += (
    'lms.djangoapps.courseware.field_overrides:OverrideModulestoreFieldData.wrap',
)

MODULESTORE_FIELD_OVERRIDE_PROVIDERS += (
    'lms.djangoapps.courseware.self_paced_overrides.SelfPacedDateOverrideProvider',
)

# PROFILE IMAGE CONFIG
PROFILE_IMAGE_DEFAULT_FILENAME = 'images/profiles/default'
PROFILE_IMAGE_SIZES_MAP = ENV_TOKENS.get(
    'PROFILE_IMAGE_SIZES_MAP',
    PROFILE_IMAGE_SIZES_MAP
)

##### Credit Provider Integration #####

CREDIT_PROVIDER_SECRET_KEYS = AUTH_TOKENS.get("CREDIT_PROVIDER_SECRET_KEYS", {})

##################### LTI Provider #####################
if FEATURES.get('ENABLE_LTI_PROVIDER'):
    INSTALLED_APPS.append('lms.djangoapps.lti_provider.apps.LtiProviderConfig')
    AUTHENTICATION_BACKENDS.append('lms.djangoapps.lti_provider.users.LtiBackend')

LTI_USER_EMAIL_DOMAIN = ENV_TOKENS.get('LTI_USER_EMAIL_DOMAIN', 'lti.example.com')

# For more info on this, see the notes in common.py
LTI_AGGREGATE_SCORE_PASSBACK_DELAY = ENV_TOKENS.get(
    'LTI_AGGREGATE_SCORE_PASSBACK_DELAY', LTI_AGGREGATE_SCORE_PASSBACK_DELAY
)

##################### Credit Provider help link ####################

#### JWT configuration ####
JWT_AUTH.update(ENV_TOKENS.get('JWT_AUTH', {}))
JWT_AUTH.update(AUTH_TOKENS.get('JWT_AUTH', {}))

# Offset for pk of courseware.StudentModuleHistoryExtended
STUDENTMODULEHISTORYEXTENDED_OFFSET = ENV_TOKENS.get(
    'STUDENTMODULEHISTORYEXTENDED_OFFSET', STUDENTMODULEHISTORYEXTENDED_OFFSET
)

################################ Settings for Credentials Service ################################

CREDENTIALS_GENERATION_ROUTING_KEY = ENV_TOKENS.get('CREDENTIALS_GENERATION_ROUTING_KEY', DEFAULT_PRIORITY_QUEUE)

# Queue to use for award program certificates
PROGRAM_CERTIFICATES_ROUTING_KEY = ENV_TOKENS.get('PROGRAM_CERTIFICATES_ROUTING_KEY', DEFAULT_PRIORITY_QUEUE)
SOFTWARE_SECURE_VERIFICATION_ROUTING_KEY = ENV_TOKENS.get(
    'SOFTWARE_SECURE_VERIFICATION_ROUTING_KEY',
    HIGH_PRIORITY_QUEUE
)

API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get('API_ACCESS_MANAGER_EMAIL')
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get('API_ACCESS_FROM_EMAIL')

############## OPEN EDX ENTERPRISE SERVICE CONFIGURATION ######################
# The Open edX Enterprise service is currently hosted via the LMS container/process.
# However, for all intents and purposes this service is treated as a standalone IDA.
# These configuration settings are specific to the Enterprise service and you should
# not find references to them within the edx-platform project.

# Publicly-accessible enrollment URL, for use on the client side.
ENTERPRISE_PUBLIC_ENROLLMENT_API_URL = ENV_TOKENS.get(
    'ENTERPRISE_PUBLIC_ENROLLMENT_API_URL',
    (LMS_ROOT_URL or '') + LMS_ENROLLMENT_API_PATH
)

# Enrollment URL used on the server-side.
ENTERPRISE_ENROLLMENT_API_URL = ENV_TOKENS.get(
    'ENTERPRISE_ENROLLMENT_API_URL',
    (LMS_INTERNAL_ROOT_URL or '') + LMS_ENROLLMENT_API_PATH
)

# Enterprise logo image size limit in KB's
ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE = ENV_TOKENS.get(
    'ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE',
    ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE
)

# Course enrollment modes to be hidden in the Enterprise enrollment page
# if the "Hide audit track" flag is enabled for an EnterpriseCustomer
ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES = ENV_TOKENS.get(
    'ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES',
    ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES
)

# A support URL used on Enterprise landing pages for when a warning
# message goes off.
ENTERPRISE_SUPPORT_URL = ENV_TOKENS.get(
    'ENTERPRISE_SUPPORT_URL',
    ENTERPRISE_SUPPORT_URL
)

# A default dictionary to be used for filtering out enterprise customer catalog.
ENTERPRISE_CUSTOMER_CATALOG_DEFAULT_CONTENT_FILTER = ENV_TOKENS.get(
    'ENTERPRISE_CUSTOMER_CATALOG_DEFAULT_CONTENT_FILTER',
    ENTERPRISE_CUSTOMER_CATALOG_DEFAULT_CONTENT_FILTER
)
INTEGRATED_CHANNELS_API_CHUNK_TRANSMISSION_LIMIT = ENV_TOKENS.get(
    'INTEGRATED_CHANNELS_API_CHUNK_TRANSMISSION_LIMIT',
    INTEGRATED_CHANNELS_API_CHUNK_TRANSMISSION_LIMIT
)

############## ENTERPRISE SERVICE API CLIENT CONFIGURATION ######################
# The LMS communicates with the Enterprise service via the requests.Session() client
# The below environmental settings are utilized by the LMS when interacting with
# the service, and override the default parameters which are defined in common.py

DEFAULT_ENTERPRISE_API_URL = None
if LMS_INTERNAL_ROOT_URL is not None:
    DEFAULT_ENTERPRISE_API_URL = LMS_INTERNAL_ROOT_URL + '/enterprise/api/v1/'
ENTERPRISE_API_URL = ENV_TOKENS.get('ENTERPRISE_API_URL', DEFAULT_ENTERPRISE_API_URL)

DEFAULT_ENTERPRISE_CONSENT_API_URL = None
if LMS_INTERNAL_ROOT_URL is not None:
    DEFAULT_ENTERPRISE_CONSENT_API_URL = LMS_INTERNAL_ROOT_URL + '/consent/api/v1/'
ENTERPRISE_CONSENT_API_URL = ENV_TOKENS.get('ENTERPRISE_CONSENT_API_URL', DEFAULT_ENTERPRISE_CONSENT_API_URL)

ENTERPRISE_SERVICE_WORKER_USERNAME = ENV_TOKENS.get(
    'ENTERPRISE_SERVICE_WORKER_USERNAME',
    ENTERPRISE_SERVICE_WORKER_USERNAME
)
ENTERPRISE_API_CACHE_TIMEOUT = ENV_TOKENS.get(
    'ENTERPRISE_API_CACHE_TIMEOUT',
    ENTERPRISE_API_CACHE_TIMEOUT
)
ENTERPRISE_CATALOG_INTERNAL_ROOT_URL = ENV_TOKENS.get(
    'ENTERPRISE_CATALOG_INTERNAL_ROOT_URL',
    ENTERPRISE_CATALOG_INTERNAL_ROOT_URL
)

CHAT_COMPLETION_API = ENV_TOKENS.get('CHAT_COMPLETION_API', '')
CHAT_COMPLETION_API_KEY = ENV_TOKENS.get('CHAT_COMPLETION_API_KEY', '')
LEARNER_ENGAGEMENT_PROMPT_FOR_ACTIVE_CONTRACT = ENV_TOKENS.get('LEARNER_ENGAGEMENT_PROMPT_FOR_ACTIVE_CONTRACT', '')
LEARNER_ENGAGEMENT_PROMPT_FOR_NON_ACTIVE_CONTRACT = ENV_TOKENS.get(
    'LEARNER_ENGAGEMENT_PROMPT_FOR_NON_ACTIVE_CONTRACT',
    ''
)
LEARNER_PROGRESS_PROMPT_FOR_ACTIVE_CONTRACT = ENV_TOKENS.get('LEARNER_PROGRESS_PROMPT_FOR_ACTIVE_CONTRACT', '')
LEARNER_PROGRESS_PROMPT_FOR_NON_ACTIVE_CONTRACT = ENV_TOKENS.get('LEARNER_PROGRESS_PROMPT_FOR_NON_ACTIVE_CONTRACT', '')

############## ENTERPRISE SERVICE LMS CONFIGURATION ##################################
# The LMS has some features embedded that are related to the Enterprise service, but
# which are not provided by the Enterprise service. These settings override the
# base values for the parameters as defined in common.py

ENTERPRISE_PLATFORM_WELCOME_TEMPLATE = ENV_TOKENS.get(
    'ENTERPRISE_PLATFORM_WELCOME_TEMPLATE',
    ENTERPRISE_PLATFORM_WELCOME_TEMPLATE
)
ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE = ENV_TOKENS.get(
    'ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE',
    ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE
)
ENTERPRISE_TAGLINE = ENV_TOKENS.get(
    'ENTERPRISE_TAGLINE',
    ENTERPRISE_TAGLINE
)
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS = set(
    ENV_TOKENS.get(
        'ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS',
        ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS
    )
)
BASE_COOKIE_DOMAIN = ENV_TOKENS.get(
    'BASE_COOKIE_DOMAIN',
    BASE_COOKIE_DOMAIN
)
SYSTEM_TO_FEATURE_ROLE_MAPPING = ENV_TOKENS.get(
    'SYSTEM_TO_FEATURE_ROLE_MAPPING',
    SYSTEM_TO_FEATURE_ROLE_MAPPING
)

# Add an ICP license for serving content in China if your organization is registered to do so
ICP_LICENSE = ENV_TOKENS.get('ICP_LICENSE', None)
ICP_LICENSE_INFO = ENV_TOKENS.get('ICP_LICENSE_INFO', {})

# How long to cache OpenAPI schemas and UI, in seconds.
OPENAPI_CACHE_TIMEOUT = ENV_TOKENS.get('OPENAPI_CACHE_TIMEOUT', 60 * 60)

########################## Parental controls config  #######################

# The age at which a learner no longer requires parental consent, or None
# if parental consent is never required.
PARENTAL_CONSENT_AGE_LIMIT = ENV_TOKENS.get(
    'PARENTAL_CONSENT_AGE_LIMIT',
    PARENTAL_CONSENT_AGE_LIMIT
)

########################## Extra middleware classes  #######################

# Allow extra middleware classes to be added to the app through configuration.
MIDDLEWARE.extend(ENV_TOKENS.get('EXTRA_MIDDLEWARE_CLASSES', []))

################# Settings for the maintenance banner #################
MAINTENANCE_BANNER_TEXT = ENV_TOKENS.get('MAINTENANCE_BANNER_TEXT', None)

########################## limiting dashboard courses ######################
DASHBOARD_COURSE_LIMIT = ENV_TOKENS.get('DASHBOARD_COURSE_LIMIT', None)

######################## Setting for content libraries ########################
MAX_BLOCKS_PER_CONTENT_LIBRARY = ENV_TOKENS.get('MAX_BLOCKS_PER_CONTENT_LIBRARY', MAX_BLOCKS_PER_CONTENT_LIBRARY)

########################## Derive Any Derived Settings  #######################

derive_settings(__name__)

############################### Plugin Settings ###############################

# This is at the bottom because it is going to load more settings after base settings are loaded

# Load production.py in plugins
add_plugins(__name__, ProjectType.LMS, SettingsType.PRODUCTION)

############## Settings for Completion API #########################

# Once a user has watched this percentage of a video, mark it as complete:
# (0.0 = 0%, 1.0 = 100%)
COMPLETION_VIDEO_COMPLETE_PERCENTAGE = ENV_TOKENS.get('COMPLETION_VIDEO_COMPLETE_PERCENTAGE',
                                                      COMPLETION_VIDEO_COMPLETE_PERCENTAGE)
COMPLETION_BY_VIEWING_DELAY_MS = ENV_TOKENS.get('COMPLETION_BY_VIEWING_DELAY_MS',
                                                COMPLETION_BY_VIEWING_DELAY_MS)

################# Settings for brand logos. #################
LOGO_URL = ENV_TOKENS.get('LOGO_URL', LOGO_URL)
LOGO_URL_PNG = ENV_TOKENS.get('LOGO_URL_PNG', LOGO_URL_PNG)
LOGO_TRADEMARK_URL = ENV_TOKENS.get('LOGO_TRADEMARK_URL', LOGO_TRADEMARK_URL)
FAVICON_URL = ENV_TOKENS.get('FAVICON_URL', FAVICON_URL)

######################## CELERY ROUTING ########################

# Defines alternate environment tasks, as a dict of form { task_name: alternate_queue }
ALTERNATE_ENV_TASKS = {}

# Defines the task -> alternate worker queue to be used when routing.
EXPLICIT_QUEUES = {
    'openedx.core.djangoapps.content.course_overviews.tasks.async_course_overview_update': {
        'queue': GRADES_DOWNLOAD_ROUTING_KEY},
    'lms.djangoapps.bulk_email.tasks.send_course_email': {
        'queue': BULK_EMAIL_ROUTING_KEY},
    'openedx.core.djangoapps.heartbeat.tasks.sample_task': {
        'queue': HEARTBEAT_CELERY_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.calculate_grades_csv': {
        'queue': GRADES_DOWNLOAD_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.calculate_problem_grade_report': {
        'queue': GRADES_DOWNLOAD_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.generate_certificates': {
        'queue': GRADES_DOWNLOAD_ROUTING_KEY},
    'lms.djangoapps.verify_student.tasks.send_verification_status_email': {
        'queue': ACE_ROUTING_KEY},
    'lms.djangoapps.verify_student.tasks.send_ace_message': {
        'queue': ACE_ROUTING_KEY},
    'lms.djangoapps.verify_student.tasks.send_request_to_ss_for_user': {
        'queue': SOFTWARE_SECURE_VERIFICATION_ROUTING_KEY},
    'openedx.core.djangoapps.schedules.tasks._recurring_nudge_schedule_send': {
        'queue': ACE_ROUTING_KEY},
    'openedx.core.djangoapps.schedules.tasks._upgrade_reminder_schedule_send': {
        'queue': ACE_ROUTING_KEY},
    'openedx.core.djangoapps.schedules.tasks._course_update_schedule_send': {
        'queue': ACE_ROUTING_KEY},
    'openedx.core.djangoapps.schedules.tasks.v1.tasks.send_grade_to_credentials': {
        'queue': CREDENTIALS_GENERATION_ROUTING_KEY},
    'common.djangoapps.entitlements.tasks.expire_old_entitlements': {
        'queue': ENTITLEMENTS_EXPIRATION_ROUTING_KEY},
    'lms.djangoapps.grades.tasks.recalculate_course_and_subsection_grades_for_user': {
        'queue': POLICY_CHANGE_GRADES_ROUTING_KEY},
    'lms.djangoapps.grades.tasks.recalculate_subsection_grade_v3': {
        'queue': SINGLE_LEARNER_COURSE_REGRADE_ROUTING_KEY},
    'openedx.core.djangoapps.programs.tasks.award_program_certificates': {
        'queue': PROGRAM_CERTIFICATES_ROUTING_KEY},
    'openedx.core.djangoapps.programs.tasks.revoke_program_certificates': {
        'queue': PROGRAM_CERTIFICATES_ROUTING_KEY},
    'openedx.core.djangoapps.programs.tasks.update_certificate_available_date_on_course_update': {
        'queue': PROGRAM_CERTIFICATES_ROUTING_KEY},
    'openedx.core.djangoapps.programs.tasks.award_course_certificate': {
        'queue': PROGRAM_CERTIFICATES_ROUTING_KEY},
    'openassessment.workflow.tasks.update_workflows_for_all_blocked_submissions_task': {
        'queue': ORA_WORKFLOW_UPDATE_ROUTING_KEY},
    'openassessment.workflow.tasks.update_workflows_for_course_task': {
        'queue': ORA_WORKFLOW_UPDATE_ROUTING_KEY},
    'openassessment.workflow.tasks.update_workflows_for_ora_block_task': {
        'queue': ORA_WORKFLOW_UPDATE_ROUTING_KEY},
    'openassessment.workflow.tasks.update_workflow_for_submission_task': {
        'queue': ORA_WORKFLOW_UPDATE_ROUTING_KEY},

}

LOGO_IMAGE_EXTRA_TEXT = ENV_TOKENS.get('LOGO_IMAGE_EXTRA_TEXT', '')

############## XBlock extra mixins ############################
XBLOCK_MIXINS += tuple(XBLOCK_EXTRA_MIXINS)

############## Settings for course import olx validation ############################
COURSE_OLX_VALIDATION_STAGE = ENV_TOKENS.get('COURSE_OLX_VALIDATION_STAGE', COURSE_OLX_VALIDATION_STAGE)
COURSE_OLX_VALIDATION_IGNORE_LIST = ENV_TOKENS.get(
    'COURSE_OLX_VALIDATION_IGNORE_LIST',
    COURSE_OLX_VALIDATION_IGNORE_LIST
)

################# show account activate cta after register ########################
SHOW_ACCOUNT_ACTIVATION_CTA = ENV_TOKENS.get('SHOW_ACCOUNT_ACTIVATION_CTA', SHOW_ACCOUNT_ACTIVATION_CTA)

################# Discussions micro frontend URL ########################
DISCUSSIONS_MICROFRONTEND_URL = ENV_TOKENS.get('DISCUSSIONS_MICROFRONTEND_URL', DISCUSSIONS_MICROFRONTEND_URL)

################### Discussions micro frontend Feedback URL###################
DISCUSSIONS_MFE_FEEDBACK_URL = ENV_TOKENS.get('DISCUSSIONS_MFE_FEEDBACK_URL', DISCUSSIONS_MFE_FEEDBACK_URL)

############################ AI_TRANSLATIONS URL ##################################
AI_TRANSLATIONS_API_URL = ENV_TOKENS.get('AI_TRANSLATIONS_API_URL', AI_TRANSLATIONS_API_URL)

############## DRF overrides ##############
REST_FRAMEWORK.update(ENV_TOKENS.get('REST_FRAMEWORK', {}))

############################# CELERY ############################
CELERY_IMPORTS.extend(ENV_TOKENS.get('CELERY_EXTRA_IMPORTS', []))

# keys for  big blue button live provider
COURSE_LIVE_GLOBAL_CREDENTIALS["BIG_BLUE_BUTTON"] = {
    "KEY": ENV_TOKENS.get('BIG_BLUE_BUTTON_GLOBAL_KEY', None),
    "SECRET": ENV_TOKENS.get('BIG_BLUE_BUTTON_GLOBAL_SECRET', None),
    "URL": ENV_TOKENS.get('BIG_BLUE_BUTTON_GLOBAL_URL', None),
}

AVAILABLE_DISCUSSION_TOURS = ENV_TOKENS.get('AVAILABLE_DISCUSSION_TOURS', [])

############## NOTIFICATIONS EXPIRY ##############
NOTIFICATIONS_EXPIRY = ENV_TOKENS.get('NOTIFICATIONS_EXPIRY', NOTIFICATIONS_EXPIRY)

############## Event bus producer ##############
EVENT_BUS_PRODUCER_CONFIG = merge_producer_configs(EVENT_BUS_PRODUCER_CONFIG,
                                                   ENV_TOKENS.get('EVENT_BUS_PRODUCER_CONFIG', {}))
BEAMER_PRODUCT_ID = ENV_TOKENS.get('BEAMER_PRODUCT_ID', BEAMER_PRODUCT_ID)
# @@@@@@@@@ tutor production.py
# -*- coding: utf-8 -*-
import os

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,

}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{

  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
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
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "Kyle's Open edX - http://local.edly.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

try:
    from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
    warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
    warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)
except ImportError:
    # REMOVE-AFTER-V18:
    # In Quince, edx-platform uses Django 5. But on master, edx-platform still uses Django 3.
    # So, Tutor v17 needs to silence these warnings, whereas Tutor v17-nightly fails to import them.
    # Once edx-platform master is upgraded to Django 5, the try-except wrapper can be removed.
    pass

warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="boto.plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="botocore.vendored.requests.packages.urllib3._collections")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs.opener")
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.edly.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "o5wToOrEitfAxwP8E5U0n5zi"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "OmweNydMBC_YOib6WZM4ph76gwT9sfvYn6qFAdFRS-PiGgyJC-6YSsY2VVViGpcbXaLcnykSv6_pvQL4PW-8XLuqylKbRlQDBX1ud-IbAAaEGBmRAW2_jfR11QH4gNmiORgrHFUe-eDghvdz6DpSTpAPDSUiSPhjDluAJ4Ya6vBkul7lITj7KdruWpb6XynxqO8dmqPv5xX112DVJSOd7sb33O8B3P7i41AD26E-117oo0zJRVZHv7DKFM23eYLBubaXQ4L0TYAJSqktniv-7Fc5cmwtTm5EeefWwun4uv6D_qVhLi0wQ0lHTx4eKi4uLkYvdTdLwqSl_GdCy4ZooQ",
        "n": "kOvj-HTtKIpBcZfwMR9Mt1L89RqiT4wjJjUk-pipRSgYebBD1Pl9oS6jIVRfMM8HN15mHAnw0GQ-Szy1PR830Ro8IjzABMyUnV0s0U0yNoJYlquiJ-jBIXzM5Ekm5vGmfoftmDT557xZ1znRGV6iVEiwF3Ng6quBtmwfMO9lcPEHhBrrHQchdC-boPiqQZmHocy-eHUgXqnZ752t3-x0cqenIBo-3ueefxAnZAm2YnT4-v3RItDuZa5mchFUO9UL4ZpFZ7GoabddlXCsYqymXylrU13IwbS6Lh00C-7sm9_lcJTRzqVBtx2DU2KTxh1fATs1A4G89anYVbpH1Ntyfw",
        "p": "vctSrWpidXYVcf9RjhB1Ok_Ye2xwkK9u99YIBxu0Dh-4q79OFhYTBgLqjz1DXa0quSf92z5Xf41d2NWnd5VWktZUg4Zrqsrc2NOlXZcwbb-XD41sweC3xQL_uB8RdUswkxlW065XXDC0MZD6_hUCYIVBJSdrM8ZTlAndad0RlbM",
        "q": "w3lqaVa58k_S2E0ldB1BcMGcI6KyLL5T6YdSogTSyKt87cZbEtjehNoRwg2IRSr7kcbuoUMWlpeVLWWcZnuu2dHKYSg4ACyXFykZtqyKUZSe-fgyEPg1ZpL8JTIelXW-y8x5LbnXsr8tfWXL9PUVpFPbsn8KePcOP1M2_QZ3YgU",
        "dq": "eNYYqu-a2SjxPRdLnODs8EgvPnQ30qMBem5V7aQvrS8ddltVN2xq-hNYQO5em-t7Ql2IbJXtY8Bmzn5u1YeFyk7-3Vqga7Mk34NfyuYUR2Qpdnswb_8P-83HIzM9ZsU34gIPsu2cYnn-I_OGxnGvJDtWp5wTHD4VR54ocvfJWwU",
        "dp": "rOYoCHENBwKu4K3-ZtQZZyjMBwwvs68OAVsK7ybOrbs6KcPaaAZuCCDp-9mMoC8b55dGDM_LOBjZsKpaqHb0ako0rajsNqgd7q1ITW1pIeHSxMlKlYiZATINMXekGN2Jf8gqsCZ30TVRQoJYFNWg17stMKKrZ3w6MXeXLFTHKz8",
        "qi": "KYhS58SxpzaojYS5sfXIhLEtAja0MerYU8cDHMwHrYw6_VZ8OxKErIUp_hrE-wJwF9YaWRbUh55Ys1eEKH6aKvSK2G2tUCXR7-320uUZeh7orOiWYAYTrn9RGc2hyFpeabL-QrIy9h4nrEPJwchc2ybQsgSJfHYWuwkT2hcK8bM",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "kOvj-HTtKIpBcZfwMR9Mt1L89RqiT4wjJjUk-pipRSgYebBD1Pl9oS6jIVRfMM8HN15mHAnw0GQ-Szy1PR830Ro8IjzABMyUnV0s0U0yNoJYlquiJ-jBIXzM5Ekm5vGmfoftmDT557xZ1znRGV6iVEiwF3Ng6quBtmwfMO9lcPEHhBrrHQchdC-boPiqQZmHocy-eHUgXqnZ752t3-x0cqenIBo-3ueefxAnZAm2YnT4-v3RItDuZa5mchFUO9UL4ZpFZ7GoabddlXCsYqymXylrU13IwbS6Lh00C-7sm9_lcJTRzqVBtx2DU2KTxh1fATs1A4G89anYVbpH1Ntyfw",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.edly.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "o5wToOrEitfAxwP8E5U0n5zi"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
# Note: CORS_ALLOW_HEADERS is intentionally not defined here, because it should
# be consistent across deployments, and is therefore set in edx-platform.

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.local.edly.io"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "hidden"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"
BULK_EMAIL_SEND_USING_EDX_ACE = True
FEATURES["ENABLE_FOOTER_MOBILE_APP_LINKS"] = False

# Branding
MOBILE_STORE_ACE_URLS = {}
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}

# Make it possible to hide courses by default from the studio
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False

# Caching
CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_lms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_lms",
}

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

MFE_CONFIG_OVERRIDES.setdefault('course-authoring', {})['LIBRARY_MODE'] = 'mixed'
# MFE: enable API and set a low cache timeout for the settings. otherwise, weird
# configuration bugs occur. Also, the view is not costly at all, and it's also cached on
# the frontend. (5 minutes, hardcoded)
ENABLE_MFE_CONFIG_API = True
MFE_CONFIG_API_CACHE_TIMEOUT = 1

# MFE-specific settings

FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = True




######## End of common LMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("LMS_BASE"),
    FEATURES["PREVIEW_LMS_BASE"],
    "lms",
]
CORS_ORIGIN_WHITELIST.append("http://local.edly.io")


# When we cannot provide secure session/csrf cookies, we must disable samesite=none
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"


# CMS authentication
IDA_LOGOUT_URI_LIST.append("http://studio.local.edly.io/logout/")

# Required to display all courses on start page
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

# Dynamic config API settings
# https://openedx.github.io/frontend-platform/module-Config.html
MFE_CONFIG = {
    "BASE_URL": "apps.local.edly.io",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "CREDENTIALS_BASE_URL": "",
    "DISCOVERY_API_BASE_URL": "",
    "FAVICON_URL": "http://local.edly.io/favicon.ico",
    "INFO_EMAIL": "contact@local.overhang.io",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "http://local.edly.io",
    "LOGIN_URL": "http://local.edly.io/login",
    "LOGO_URL": "http://local.edly.io/theming/asset/images/logo.png",
    "LOGO_WHITE_URL": "http://local.edly.io/theming/asset/images/logo.png",
    "LOGO_TRADEMARK_URL": "http://local.edly.io/theming/asset/images/logo.png",
    "LOGOUT_URL": "http://local.edly.io/logout",
    "MARKETING_SITE_BASE_URL": "http://local.edly.io",
    "PASSWORD_RESET_SUPPORT_LINK": "mailto:contact@local.overhang.io",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "http://local.edly.io/login_refresh",
    "SITE_NAME": "Kyle's Open edX",
    "STUDIO_BASE_URL": "http://studio.local.edly.io",
    "USER_INFO_COOKIE_NAME": "user-info",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
}

# MFE-specific settings


AUTHN_MICROFRONTEND_URL = "http://apps.local.edly.io/authn"
AUTHN_MICROFRONTEND_DOMAIN  = "apps.local.edly.io/authn"
MFE_CONFIG["DISABLE_ENTERPRISE_LOGIN"] = True





MFE_CONFIG["COURSE_AUTHORING_MICROFRONTEND_URL"] = "http://apps.local.edly.io/course-authoring"
MFE_CONFIG["ENABLE_ASSETS_PAGE"] = "true"
MFE_CONFIG["ENABLE_HOME_PAGE_COURSE_API_V2"] = "true"
MFE_CONFIG["ENABLE_PROGRESS_GRAPH_SETTINGS"] = "true"
MFE_CONFIG["ENABLE_TAGGING_TAXONOMY_PAGES"] = "true"









LEARNING_MICROFRONTEND_URL = "http://apps.local.edly.io/learning"
MFE_CONFIG["LEARNING_BASE_URL"] = "http://apps.local.edly.io/learning"








LOGIN_REDIRECT_WHITELIST.append("apps.local.edly.io")
CORS_ORIGIN_WHITELIST.append("http://apps.local.edly.io")
CSRF_TRUSTED_ORIGINS.append("http://apps.local.edly.io")



class Flag:

    def __init__(self, *, default: bool, name: str | None = None):
        self.default = default
        self._name = name
        self._cache: bool | None = None

    @cached_property
    def name(self) -> str:
        if self._name:
            return self._name
        for setting_name, setting_value in vars(settings).items():
            if setting_value is self:
                return setting_name
        raise

    @cached_property
    def value(self) -> bool:
        if settings.FLAG_OVERRIDES_ENABLED:
            for override in FlagOverrides.objects.get(name=name)
                if override.applies_to_current_request():
                    return override.value
        return self.default

    def __bool__(self) -> bool:
        return self.value


ENABLE_CONTENT_LIBRARIES = Flag(default=True)


MY_EXPERIMENT_1 = Experiment([Flag(default)])

