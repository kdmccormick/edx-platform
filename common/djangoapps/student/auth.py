"""
The application interface to roles which checks whether any user trying to change
authorization has authorization to do so, which infers authorization via role hierarchy
(GlobalStaff is superset of auths of course instructor, ...), which consults the config
to decide whether to check course creator role, and other such functions.
"""


from ccx_keys.locator import CCXBlockUsageLocator, CCXLocator
from django.conf import settings
from django.core.exceptions import PermissionDenied
from opaque_keys.edx.keys import LearningContextKey, OpaqueKey
from opaque_keys.edx.locator import LibraryLocator, LibraryLocatorV2
from typing import TypeAlias

from common.djangoapps.student.roles import (
    CourseBetaTesterRole,
    CourseCreatorRole,
    CourseInstructorRole,
    CourseLimitedStaffRole,
    CourseRole,
    CourseStaffRole,
    GlobalStaff,
    LibraryUserRole,
    OrgContentCreatorRole,
    OrgInstructorRole,
    OrgLibraryUserRole,
    OrgStaffRole
)

# Studio permissions:
STUDIO_EDIT_ROLES = 8
STUDIO_VIEW_USERS = 4
STUDIO_EDIT_CONTENT = 2
STUDIO_VIEW_CONTENT = 1
STUDIO_NO_PERMISSIONS = 0
# In addition to the above, one is always allowed to "demote" oneself to a lower role within a course, or remove oneself


# A union of the locators for learning contexts upon which it makes sense to do Studio permission checks.
# These locators all have the `org` field.
PermissionContextLocator: TypeAlias = CourseLocator | LibraryLocator | LibraryLocatorV2


def is_ccx_course(key: OpaqueKey) -> bool:
    """
    Check whether the key maps to a CCX course or a block usage within it; this is important
    because we don't allow access to CCX courses in Studio.
    """
    return isinstance(key, (CCXLocator, CCXBlockUsageLocator))


def user_has_role(user, role):
    """
    Check whether this user has access to this role (either direct or implied)
    :param user:
    :param role: an AccessRole
    """
    if not user.is_active:
        return False
    # Do cheapest check first even though it's not the direct one
    if GlobalStaff().has_user(user):
        return True
    # CourseCreator is odd b/c it can be disabled via config
    if isinstance(role, CourseCreatorRole):
        # completely shut down course creation setting
        if settings.FEATURES.get('DISABLE_COURSE_CREATION', False):
            return False
        # wide open course creation setting
        if not settings.FEATURES.get('ENABLE_CREATOR_GROUP', False):
            return True

    if role.has_user(user):
        return True
    # If not, then check inferred permissions
    if (isinstance(role, (CourseStaffRole, CourseBetaTesterRole)) and
            CourseInstructorRole(role.course_key).has_user(user)):
        return True

    return False


def get_user_permissions(user, context_key: PermissionContextLocator|None, org: str|None = None) -> bool:
    """
    Get the bitmask of permissions that this user has in the given learning context (eg, course or library).
    Can also set context_key=None and pass in an org to get the user's permissions for that organization as a whole.
    """
    if org is None:
        if not isinstance(context_key, (CourseLocator, LibraryLocator, LibraryV2Locator)):
            raise ValueError(
                f"get_user_permissions expected a locator to a course or library; got {context_key} instead."
            )
        org = context_key.org
        if isinstance(context_key, CourseKey):
            context_key = context_key.for_branch(None)
    else:
        assert context_key is None
    # No one has studio permissions for CCX courses
    if is_ccx_course(context_key):
        return STUDIO_NO_PERMISSIONS
    all_perms = STUDIO_EDIT_ROLES | STUDIO_VIEW_USERS | STUDIO_EDIT_CONTENT | STUDIO_VIEW_CONTENT
    # global staff, org instructors, and course instructors have all permissions:
    if GlobalStaff().has_user(user) or OrgInstructorRole(org=org).has_user(user):
        return all_perms
    # V2 library permissions are computed solely from tables in the content_libraries app.
    if isinstance(context_key, LibraryLocatorV2):
        return todo()
    # insturctor
    if context_key and user_has_role(user, CourseInstructorRole(context_key)):
        return all_perms
    # HACK: Limited Staff should not have studio read access. However, since many LMS views depend on the
    #  `has_course_author_access` check and `course_author_access_required` decorator, we have to allow write access
    #  until the permissions become more granular. For example, there could be STUDIO_VIEW_COHORTS and
    #  STUDIO_EDIT_COHORTS specifically for the cohorts endpoint, which is used to display the "Cohorts" tab of the
    #  Instructor Dashboard.
    #  The permissions matrix from the RBAC project (https://github.com/openedx/platform-roadmap/issues/246) shows that
    #  the LMS and Studio permissions will be separated as a part of this project. Once this is done (and this code is
    #  not removed during its implementation), we can replace the Limited Staff permissions with more granular ones.
    if context_key and user_has_role(user, CourseLimitedStaffRole(context_key)):
        return STUDIO_EDIT_CONTENT
    # Staff have all permissions except EDIT_ROLES:
    if OrgStaffRole(org=org).has_user(user) or (context_key and user_has_role(user, CourseStaffRole(context_key))):
        return STUDIO_VIEW_USERS | STUDIO_EDIT_CONTENT | STUDIO_VIEW_CONTET
    # Otherwise, for V1 libraries, users can view only:
    if context_key and isinstance(context_key, LibraryLocator):
        if OrgLibraryUserRole(org=org).has_user(user) or user_has_role(user, LibraryUserRole(context_key)):
            return STUDIO_VIEW_USERS | STUDIO_VIEW_CONTENT
    return STUDIO_NO_PERMISSIONS


def has_studio_write_access(user, context_key: PermissionContextLocator|None):
    """
    Return True if user has studio write access to the given learning context.
    Note that the CMS permissions model is with respect to courses.
    There is a super-admin permissions if user.is_staff is set.
    Also, since we're unifying the user database between LMS and CAS,
    I'm presuming that the course instructor (formally known as admin)
    will not be in both INSTRUCTOR and STAFF groups, so we have to cascade our
    queries here as INSTRUCTOR has all the rights that STAFF do.
    """
    return bool(STUDIO_EDIT_CONTENT & get_user_permissions(user, context_key: PermissionContextLocator|None))


def has_course_author_access(user, context_key: PermissionContextLocator|None):
    """
    Old name for has_studio_write_access
    """
    return has_studio_write_access(user, context_key)


def has_studio_advanced_settings_access(user):
    """
    If DISABLE_ADVANCED_SETTINGS feature is enabled, only Django Superuser
    or Django Staff can access "Advanced Settings".

    By default, this feature is disabled.
    """
    return (
        not settings.FEATURES.get('DISABLE_ADVANCED_SETTINGS', False)
        or user.is_staff
        or user.is_superuser
    )


def has_studio_read_access(user, context_key: PermissionContextLocator|None):
    """
    Return True if user is allowed to view this context (course/library) in studio.
    Will also return True if user has write access in studio (has_course_author_access)

    There is currently no such thing as read-only course access in studio, but
    there is read-only access to content libraries.
    """
    return bool(STUDIO_VIEW_CONTENT & get_user_permissions(user, context_key))


def is_content_creator(user, org):
    """
    Check if the user has the role to create content.

    This function checks if the User has role to create content
    or if the org is supplied, it checks for Org level course content
    creator.
    """
    return (user_has_role(user, CourseCreatorRole()) or
            user_has_role(user, OrgContentCreatorRole(org=org)))


def add_users(caller, role, *users):
    """
    The caller requests adding the given users to the role. Checks that the caller
    has sufficient authority.

    :param caller: a user
    :param role: an AccessRole
    """
    _check_caller_authority(caller, role)
    role.add_users(*users)


def remove_users(caller, role, *users):
    """
    The caller requests removing the given users from the role. Checks that the caller
    has sufficient authority.

    :param caller: a user
    :param role: an AccessRole
    """
    # can always remove self (at this layer)
    if not(len(users) == 1 and caller == users[0]):
        _check_caller_authority(caller, role)
    role.remove_users(*users)


def update_org_role(caller, role, user, orgs):
    """
    The caller requests updating the Org role for the user. Checks that the caller has
    sufficient authority.

    :param caller: an user
    :param role: an AccessRole class
    :param user: an user for which org roles are updated
    :param orgs: List of organization names to update the org role
    """
    _check_caller_authority(caller, role())
    existing_org_roles = set(role().get_orgs_for_user(user))
    orgs_roles_to_create = list(set(orgs) - existing_org_roles)
    org_roles_to_delete = list(existing_org_roles - set(orgs))
    for org in orgs_roles_to_create:
        role(org=org).add_users(user)
    for org in org_roles_to_delete:
        role(org=org).remove_users(user)


def _check_caller_authority(caller, role):
    """
    Internal function to check whether the caller has authority to manipulate this role
    :param caller: a user
    :param role: an AccessRole
    """
    if not (caller.is_authenticated and caller.is_active):
        raise PermissionDenied
    # superuser
    if GlobalStaff().has_user(caller):
        return

    if isinstance(role, (GlobalStaff, CourseCreatorRole, OrgContentCreatorRole)):  # lint-amnesty, pylint: disable=no-else-raise
        raise PermissionDenied
    elif isinstance(role, CourseRole):  # instructors can change the roles w/in their course
        if not user_has_role(caller, CourseInstructorRole(role.course_key)):
            raise PermissionDenied
