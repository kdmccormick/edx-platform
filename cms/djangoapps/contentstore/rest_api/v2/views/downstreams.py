"""
API Views for managing & syncing links between upstream & downstream content
"""

import edx_api_doc_tools as apidocs
from django.contrib.auth.models import AbstractUser
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import UsageKey
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.lib.xblock.upstream_sync import UpstreamLink, sync_from_upstream, BadUpstream, BadDownstream
from common.djangoapps.student.auth import has_studio_write_access, has_studio_read_access
from openedx.core.lib.api.view_utils import (
    DeveloperErrorViewMixin,
    view_auth_classes,
)
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import ItemNotFoundError


@view_auth_classes(is_authenticated=True)
class UptreamLinkView(DeveloperErrorViewMixin, APIView):
    """
    @@TODO
    """

    def get(self, request: Request, usage_key_string: str) -> Response:
        """
        @@TODO
        """
        downstream = _load_block_with_access(request.user, usage_key_string, require_write_access=False)
        return Response(UpstreamLink.try_fetch_for_block(downstream).to_json())


@view_auth_classes(is_authenticated=True)
class SyncFromUpstreamView(DeveloperErrorViewMixin, APIView):
    """
    @@TODO
    """

    def post(self, request: Request, usage_key_string: str) -> Response:
        """
        Pull latest updates to the block at {usage_key_string} from its linked upstream content.

        **Example Request**

            POST /api/contentstore/v2/downstreams/{usage_key_string}

        **Response Values**

        If the request is successful, an HTTP 200 "OK" response is returned, with no body.
        If the request fails, an HTTP 4xx response is returned, with an error message.
        """
        downstream = _load_block_with_access(request.user, usage_key_string, require_write_access=True)
        old_version = downstream.upstream_version
        try:
            sync_from_upstream(downstream, request.user, apply_updates=True)
        except (BadUpstream, BadDownstream) as exc:
            raise ValidationError(str(exc))
        store.update_item(downstream, request.user.id)
        return Response(
            f"Updated block '{usage_key_string}' from verison {old_version} "
            f"to version {downstream.upstream_version} of '{upstream_link.upstream_ref}'."
        )

    def delete(self, request: Request, usage_key_string: str) -> Response:
        """
        @@TODO
        """
        downstream = _load_block_with_access(request.user, usage_key_string, require_write_access=True)
        try:
            upstream_link = UpstreamLink.fetch_for_block(downstream)
        except (BadUpstream, BadDownstream) as exc:
            raise ValidationError(str(exc))
        downstream.declined_version = upstream_link.latest_version
        modulestore().update_item(downstream, request.user.id)
        return Response(
            f"Declined to update block '{usage_key_string}' from version {downstream.upstream_version} "
            f"to verison {downstream.declined_version} of '{upstream_link.upstream_ref}'."
        )


def _load_block_with_access(user: AbstractUser, usage_key_string: str, *, require_write_access: bool) -> XBlock:
    """
    @@TODO
    """
    not_found = NotFound(f"Block not found or not accessible: {usage_key_string}")
    try:
        usage_key = UsageKey.from_string(usage_key_string)
    except InvalidKeyError:
        raise ValidationError(f"Malformed block usage key: {usage_key_string}")
    if needs_write_access:
        if not has_studio_write_access(user, usage_key.context_key):
            if has_studio_read_access(user, usage_key.context_key):
                raise PermissionDenied(f"User lacks permission to modify block: {usage_key_string}")
            else:
                raise not_found
    else:
        if not has_studio_read_access(user, usage_key.context_key):
            raise not_found
    try:
        return modulestore().get_item(usage_key)
    except ItemNotFoundError:
        raise not_found
