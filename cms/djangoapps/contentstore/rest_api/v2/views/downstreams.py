"""
API Views for managing & syncing links between upstream & downstream content
"""

from django.contrib.auth.models import AbstractUser
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import UsageKey
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from xblock.core import XBlock

from cms.lib.xblock.upstream_sync import UpstreamLink, sync_from_upstream, decline_sync, BadUpstream, BadDownstream
from common.djangoapps.student.auth import has_studio_write_access, has_studio_read_access
from openedx.core.lib.api.view_utils import (
    DeveloperErrorViewMixin,
    view_auth_classes,
)
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import ItemNotFoundError


# TODO: Potential future view.
# @view_auth_classes(is_authenticated=True)
# class DownstreamListView(DeveloperErrorViewMixin, APIView):
#     """
#     List all blocks which are linked to upstream content, with optional filtering.
#     """
#     def get(self, request: Request) -> Response:
#         """
#         Handle the request.
#         """
#         course_key_string = request.GET['course']
#         username = request.GET['username']
#         syncable = request.GET['sync']
#         ...


@view_auth_classes(is_authenticated=True)
class DownstreamView(DeveloperErrorViewMixin, APIView):
    """
    Inspect or manage an XBlock's link to upstream content.
    """

    def get(self, request: Request, usage_key_string: str) -> Response:
        """
        Inspect an XBlock's link to upstream content.
        """
        assert isinstance(request.user, AbstractUser)
        downstream = _load_block_with_access(request.user, usage_key_string, require_write_access=False)
        link = UpstreamLink.try_fetch_for_block(downstream)
        return Response(link.to_json() if link else None)

    # TODO: Potential future methods for this path.
    # def delete(self, request: Request, usage_key_string: str) -> Response:
    #     """
    #     Sever an XBlock's link to upstream content.
    #     """
    #
    # def put(self, request: Request, usage_key_string: str) -> Response:
    #     """
    #     Edit an XBlock's link to upstream content.
    #     """


@view_auth_classes(is_authenticated=True)
class SyncFromUpstreamView(DeveloperErrorViewMixin, APIView):
    """
    Accept or decline an opportunity to sync a downstream block from its upstream content.
    """

    def post(self, request: Request, usage_key_string: str) -> Response:
        """
        Pull latest updates to the block at {usage_key_string} from its linked upstream content.
        """
        assert isinstance(request.user, AbstractUser)
        downstream = _load_block_with_access(request.user, usage_key_string, require_write_access=True)
        if not downstream.upstream:
            raise NotFound(detail=f"Block '{usage_key_string}' is not linked to a library block")
        old_version = downstream.upstream_version
        try:
            sync_from_upstream(downstream, request.user, apply_updates=True)
        except (BadUpstream, BadDownstream) as exc:
            raise ValidationError(detail=str(exc)) from exc
        modulestore().update_item(downstream, request.user.id)
        return Response(
            f"Updated block '{usage_key_string}' from verison {old_version} "
            f"to version {downstream.upstream_version} of '{downstream.upstream}'."
        )

    def delete(self, request: Request, usage_key_string: str) -> Response:
        """
        Handle the request.
        """
        assert isinstance(request.user, AbstractUser)
        downstream = _load_block_with_access(request.user, usage_key_string, require_write_access=True)
        if not downstream.upstream:
            raise NotFound(f"Block '{usage_key_string}' is not linked to a library block")
        try:
            decline_sync(downstream)
        except (BadUpstream, BadDownstream) as exc:
            raise ValidationError(str(exc)) from exc
        modulestore().update_item(downstream, request.user.id)
        return Response(
            f"Declined to update block '{usage_key_string}' from version {downstream.upstream_version} "
            f"to verison {downstream.declined_version} of '{downstream.upstream}'."
        )


def _load_block_with_access(user: AbstractUser, usage_key_string: str, *, require_write_access: bool) -> XBlock:
    """
    Given its serialized usage key, load an XBlock from modulestore, failing if user lacks read access.

    If `require_write_access`, then assert write access rather than read access.

    Raise a DRF-friendly exception if XBlock cannot be loaded.
    """
    not_found = NotFound(detail=f"Block not found or not accessible: {usage_key_string}")
    try:
        usage_key = UsageKey.from_string(usage_key_string)
    except InvalidKeyError as exc:
        raise ValidationError(detail=f"Malformed block usage key: {usage_key_string}") from exc
    if require_write_access:
        if not has_studio_write_access(user, usage_key.context_key):
            if has_studio_read_access(user, usage_key.context_key):
                # Raise a slightly more detailed 403 error for users with read access
                raise PermissionDenied(detail=f"User lacks permission to modify block: {usage_key_string}")
            raise not_found  # Users with no read access get an opaque 404 -- avoid leaking content info
    elif not has_studio_read_access(user, usage_key.context_key):
        raise not_found
    try:
        return modulestore().get_item(usage_key)
    except ItemNotFoundError as exc:
        raise not_found from exc
