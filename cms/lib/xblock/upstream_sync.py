"""
Synchronize content and settings from upstream blocks to their downstream usages.

At the time of writing, we assume that for any upstream-downstream linkage:
* The upstream is a Component from a Learning Core-backed Content Library.
* The downstream is a block of matching type in a SplitModuleStore-backed Courses.
* They are both on the same Open edX instance.

HOWEVER, those assumptions may loosen in the future. So, we consider these to be INTERNAL ASSUMPIONS that should not be
exposed through this module's public Python interface.
"""
import typing as t
from dataclasses import dataclass, asdict

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import UsageKey, CourseKey
from opaque_keys.edx.locator import LibraryUsageLocatorV2
from rest_framework.exceptions import NotFound
from xblock.exceptions import XBlockNotFoundError
from xblock.fields import Scope, String, Integer
from xblock.core import XBlockMixin, XBlock

import openedx.core.djangoapps.xblock.api as xblock_api
from openedx.core.djangoapps.content_libraries.api import get_library_block


class BadUpstream(Exception):
    """
    Reference to upstream content is malformed, invalid, and/or inaccessible.

    Should be constructed with a human-friendly, localized, PII-free message, suitable for API responses and UI display.
    """


class BadDownstream(Exception):
    """
    Downstream content does not support sync.

    Should be constructed with a human-friendly, localized, PII-free message, suitable for API responses and UI display.
    """


@dataclass(frozen=True)
class UpstreamLink:
    """
    Metadata about a downstream's relationship with an upstream.
    """
    upstream_ref: str  # Reference to the upstream content, e.g., a serialized library block usage key.
    version_synced: int  # Version of the upstream to which the downstream was last synced.
    version_available: int | None  # Latest version of the upstream that's available, or None if it couldn't be loaded.
    version_declined: int | None  # Latest version which the user has declined to sync with, if any.
    error_message: str | None

    @property
    def prompt_sync(self) -> bool:
        """
        Should we invite the downstream's authors to sync the latest upstream updates?
        """
        return bool(
            self.upstream_ref and
            self.version_available and
            self.version_available > self.version_synced and
            self.version_available > (self.version_declined or 0)
        )

    def to_json(self) -> dict[str, t.Any]:
        """
        Get an JSON-API-friendly representation of this upstream link.
        """
        return {
            **asdict(self),
            "prompt_sync": self.prompt_sync,
        }

    @classmethod
    def try_fetch_for_block(cls, downstream: XBlock) -> t.Self | None:
        """
        Same as `fetch_for_block`, but upon failure, sets `.error_message` instead of raising an exception.
        """
        try:
            return cls.fetch_for_block(downstream)
        except (BadDownstream, BadUpstream) as exc:
            return cls(
                upstream_ref=downstream.upstream,
                version_synced=downstream.upstream_version,
                version_available=None,
                version_declined=None,
                error_message=str(exc),
            )

    @classmethod
    def fetch_for_block(cls, downstream: XBlock) -> t.Self | None:
        """
        Get info on a block's relationship with its upstream without actually loading any upstream content.

        Currently, the only supported upstream are LC-backed Library Components. This may change in the future (see
        module docstring).

        Raises: BadUpstream, BadDownstream
        """
        if not downstream.upstream:
            return None
        if not isinstance(downstream.usage_key.context_key, CourseKey):
            raise BadDownstream(_("Cannot update content because it does not belong to a course."))
        if downstream.has_children:
            raise BadDownstream(_("Updating content with children is not yet supported."))
        try:
            upstream_key = LibraryUsageLocatorV2.from_string(downstream.upstream)
        except InvalidKeyError as exc:
            raise BadUpstream(_("Reference to linked library item is malformed")) from exc
        downstream_type = downstream.usage_key.block_type
        if upstream_key.block_type != downstream_type:
            # Note: Currently, we strictly enforce that the downstream and upstream block_types must exactly match.
            #       It could be reasonable to relax this requirement in the future if there's product need for it.
            #       For example, there's no reason that a StaticTabBlock couldn't take updates from an HtmlBlock.
            raise BadUpstream(
                _("Content type mismatch: {downstream_type} cannot be linked to {upstream_type}.").format(
                    downstream_type=downstream_type, upstream_type=upstream_key.block_type
                )
            ) from TypeError(
                f"downstream block '{downstream.usage_key}' is linked to "
                f"upstream block of different type '{upstream_key}'"
            )
        try:
            lib_meta = get_library_block(upstream_key)
        except XBlockNotFoundError as exc:
            raise BadUpstream(_("Linked library item was not found in the system")) from exc
        return cls(
            upstream_ref=downstream.upstream,
            version_synced=downstream.upstream_version,
            version_available=(lib_meta.published_version_num if lib_meta else None),
            version_declined=downstream.upstream_version_declined,
            error_message=None,
        )


def sync_from_upstream(downstream: XBlock, user: AbstractUser, *, apply_updates: bool) -> None:
    """
    @@TODO docstring

    Does not save `downstream` to the store. That is left up to the caller.

    Raises: BadUpstream, BadDownstream
    """
    # Try to load the upstream.
    upstream_link = UpstreamLink.fetch_for_block(downstream)  # Can raise BadUpstream or BadUpstream
    if not upstream_link:
        return  # No upstream -> nothing to sync.
    try:
        upstream = xblock_api.load_block(UsageKey.from_string(downstream.upstream), user)
    except NotFound as exc:
        raise BadUpstream(_("Linked library item could not be loaded: {}").format(downstream.upstream)) from exc

    customizable_fields = downstream.get_customizable_fields()

    # For every field:
    for field_name, field in upstream.__class__.fields.items():

        # ...(ignoring fields that aren't set in the authoring environment)...
        if field.scope not in [Scope.content, Scope.settings]:
            continue

        # if the field *can be* customized (whether or not it *has been* customized)...
        new_upstream_value = getattr(upstream, field_name)
        old_upstream_value = None
        if restore_field_name := customizable_fields.get(field.name):

            # ...then save its latest upstream value to a hidden field.
            old_upstream_value = getattr(downstream, restore_field_name)
            setattr(downstream, restore_field_name, new_upstream_value)

        # And, if we're applying updates...
        if not apply_updates:
            continue

        # ...*and* the field is non-customized...
        if field_name in customizable_fields:

            # (Determining whether a field has been customized will differ in Beta vs Future release.
            #  See "PRESRVING DOWNSTREAM CUSTOMIZATIONS" comment below for details.

            #  FUTURE BEHAVIOR: field is "customized" iff we have noticed that the user edited it.
            #  if field_name in downstream.downstream_customized:
            #      continue

            #  BETA BEHAVIOR: field is "customized" iff we have the prev upstream value, but field doesn't match it.)
            downstream_value = getattr(downstream, field_name)
            if old_upstream_value and downstream_value != old_upstream_value:
                continue

        # ... then actually apply the upstream update to the downstream block!
        setattr(downstream, field_name, new_upstream_value)

    # Done syncing. Record the latest upstream version for future reference.
    downstream.upstream_version = upstream_link.version_available


class UpstreamSyncMixin(XBlockMixin):
    """
    Allows an XBlock in the CMS to be associated & synced with an upstream.

    Mixed into CMS's XBLOCK_MIXINS, but not LMS's.
    """

    # Upstream synchronization metadata fields
    upstream = String(
        help=(
            "The usage key of a block (generally within a content library) which serves as a source of upstream "
            "updates for this block, or None if there is no such upstream. Please note: It is valid for this "
            "field to hold a usage key for an upstream block that does not exist (or does not *yet* exist) on "
            "this instance, particularly if this downstream block was imported from a different instance."
        ),
        default=None, scope=Scope.settings, hidden=True, enforce_type=True
    )
    upstream_version = Integer(
        help=(
            "Record of the upstream block's version number at the time this block was created from it. If this "
            "upstream_version is smaller than the upstream block's latest published version, then the author will be "
            "invited to sync updates into this downstream block, presuming that they have not already declined to sync "
            "said version."
        ),
        default=None, scope=Scope.settings, hidden=True, enforce_type=True,
    )
    upstream_version_declined = Integer(
        help=(
            "Record of the latest upstream version for which the author declined to sync updates, or None if they have "
            "never declined an update."
        ),
        default=None, scope=Scope.settings, hidden=True, enforce_type=True,
    )

    # Store upstream defaults for customizable fields.
    upstream_display_name = String(
        help=("The value of display_name on the linked upstream block."),
        default=None, scope=Scope.settings, hidden=True, enforce_type=True,
    )
    upstream_max_attempts = Integer(
        help=("The value of max_attempts on the linked upstream block."),
        default=None, scope=Scope.settings, hidden=True, enforce_type=True,
    )

    @classmethod
    def get_customizable_fields(cls) -> dict[str, str]:
        """
        Mapping from each customizable field to field which stores its upstream default.

        XBlocks outside of edx-platform can override this in order to set up their own customizable fields.
        """
        return {
            "display_name": "upstream_display_name",
            "max_attempts": "upstream_max_attempts",
        }

    # PRESERVING DOWNSTREAM CUSTOMIZATIONS and RESTORING UPSTREAM DEFAULTS
    #
    # For the full Content Libraries Relaunch, we would like to keep track of which customizable fields the user has
    # actually customized. The idea is: once an author has customized a customizable field....
    #
    #   - future upstream syncs will NOT blow away the customization,
    #   - but future upstream syncs WILL tuck the new upstream default value away in a hidden field,
    #   - and the author can can revert back to said upstream default value at any point.
    #
    # Now, whether field is "customized" (and thus "revertible") is dependent on whether they have ever edited it.
    # To instrument this, we need to keep track of which customizable fields have been edited using a new XBlock field:
    # `downstream_customized`
    #
    # Implementing `downstream_customized` has proven difficult, because there is no simple way to keep it up-to-date
    # with the many different ways XBlock fields can change. The `.save()` and `.editor_saved()` methods are promising,
    # but we need to do more due diligence to be sure that they cover all cases, including API edits, import/export,
    # copy/paste, etc. We will figure this out in time for the full Content Libraries Relaunch (related ticket:
    # https://github.com/openedx/frontend-app-authoring/issues/1317). But, for the Beta realease, we're going to
    # implement something simpler:
    #
    # - We keep the upstream defaults tucked away in a hidden field (same as above).
    # - If a customizable field DOES match the upstream default, then future upstream syncs DO update it.
    # - If a customizable field does NOT the upstream default, then future upstream syncs DO NOT update it.
    # - There is no UI option for explicitly reverting back to the upstream default.
    #
    # For future reference, here is a partial implementation of what we are thinking for the full Content Libraries
    # Relaunch::
    #
    #    downstream_customized = List(
    #        help=(
    #            "Names of the fields which have values set on the upstream block yet have been explicitly "
    #            "overridden on this downstream block. Unless explicitly cleared by the user, these customizations "
    #            "will persist even when updates are synced from the upstream."
    #        ),
    #        default=[], scope=Scope.settings, hidden=True, enforce_type=True,
    #    )
    #
    #    def save(self, *args, **kwargs):
    #        """
    #        Update `downstream_customized` when a customizable field is modified.
    #
    #        NOTE: This does not work, because save() isn't actually called in all the cases that we'd want it to be.
    #        """
    #        super().save(*args, **kwargs)
    #        customizable_fields = self.get_customizable_fields()
    #
    #        # Loop through all the fields that are potentially cutomizable.
    #        for field_name, restore_field_name in self.get_customizable_fields():
    #
    #            # If the field is already marked as customized, then move on so that we don't
    #            # unneccessarily query the block for its current value.
    #            if field_name in self.downstream_customized:
    #                continue
    #
    #            # If this field's value doesn't match the synced upstream value, then mark the field
    #            # as customized so that we don't clobber it later when syncing.
    #            # NOTE: Need to consider the performance impact of all these field lookups.
    #            if getattr(self, field_name) != getattr(self, restore_field_name):
    #                self.downstream_customized.append(field_name)
