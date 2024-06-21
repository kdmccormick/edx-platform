"""
Mixin class that provides authoring capabilities for XBlocks.
"""


import logging

from django.conf import settings
from web_fragments.fragment import Fragment
from xblock.core import XBlock, XBlockMixin
from xblock.fields import String, Scope

log = logging.getLogger(__name__)

VISIBILITY_VIEW = 'visibility_view'


@XBlock.needs("i18n")
@XBlock.needs("mako")
class AuthoringMixin(XBlockMixin):
    """
    Mixin class that provides authoring capabilities for XBlocks.
    """
    def _get_studio_resource_url(self, relative_url):
        """
        Returns the Studio URL to a static resource.
        """
        return settings.STATIC_URL + relative_url

    def visibility_view(self, _context=None):
        """
        Render the view to manage an xblock's visibility settings in Studio.
        Args:
            _context: Not actively used for this view.
        Returns:
            (Fragment): An HTML fragment for editing the visibility of this XBlock.
        """
        fragment = Fragment()
        from cms.djangoapps.contentstore.utils import reverse_course_url
        fragment.add_content(self.runtime.service(self, 'mako').render_cms_template('visibility_editor.html', {
            'xblock': self,
            'manage_groups_url': reverse_course_url('group_configurations_list_handler', self.location.course_key),
        }))
        fragment.add_javascript_url(self._get_studio_resource_url('/js/xblock/authoring.js'))
        fragment.initialize_js('VisibilityEditorInit')
        return fragment

    copied_from_block = String(
        # Note: used by the content_staging app. This field is not needed in the LMS.
        help="ID of the block that this one was copied from, if any. Used when copying and pasting blocks in Studio.",
        scope=Scope.settings,
        enforce_type=True,
    )

    ##########################
    # BEGIN CONTENT SYNC STUFF
    # @@TODO move?
    ##########################
    from xblock.fields import String, Integer, List, Dict
    from opaque_keys.edx.keys import UsageKey

    upstream = String(
        scope=Scope.settings,
        help=(
            "The usage key of a block (generally within a Content Library) which serves as a source of upstream "
            "updates for this block, or None if there is no such upstream. Please note: It is valid for upstream_block "
            "to hold a usage key for a block that does not exist (or does not *yet* exist) on this instance, "
            "particularly if this block was imported from a different instance."
        ),
        hidden=True,
        default=None,
        enforce_type=True,
    )
    upstream_version = Integer(
        scope=Scope.settings,
        help=(
            "The upstream_block's version number, at the time this block was created from it. "
            "If this version is older than the upstream_block's latest version, then CMS will "
            "allow this block to fetch updated content from upstream_block."
        ),
        hidden=True,
        default=None,
        enforce_type=True,
    )
    upstream_overridden = List(
        scope=Scope.settings,
        help=(
            "@@TODO"
        ),
        hidden=True,
        default=[],
        enforce_type=True,
    )
    upstream_settings = Dict(
        scope=Scope.settings,
        help=(
            "@@TODO"
        ),
        hidden=True,
        default={},
        enforce_type=True,
    )

    def set_upstream(self, upstream_key: UsageKey, user_id: int) -> None:
        """
        @@TODO
        """
        self.upstream = str(upstream_key)
        self._sync_with_upstream(user_id=user_id, apply_updates=False)

    def _sync_with_upstream(self, *, user_id: int, apply_updates: bool) -> None:
        """
        @@TODO
        """
        upstream_key = UsageKey.from_string(self.upstream)
        assert is_block_valid_upstream(upstream_key)
        from openedx.core.djangoapps.content_libraries.api import get_library_block
        from django.contrib.auth import get_user_model
        from openedx.core.djangoapps.xblock.api import load_block
        self.upstream_settings = {}
        try:
            print("3==================")
            upstream = load_block(upstream_key, get_user_model().objects.get(id=user_id))
            upstream_version = get_library_block(upstream_key).version_num
        except:  # @@TODO handle missing
            print("4a=================")
            self.upstream_version = None
            raise
            return
        print("4==================")
        self.upstream_version = upstream_version
        for field_name, field in upstream.fields.items():
            if field.scope == Scope.settings:
                value = getattr(upstream, field_name)
                self.upstream_settings[field_name] = value
                print(field_name)
                if apply_updates and field_name not in self.upstream_overidden:
                    setattr(self, field_name, value)
        print("5==================")
        print(self.upstream_settings)

    #@XBlock.json_handler
    #def upstream_info(self, _data=None, _suffix=None):
    #    """
    #    @@TODO write this
    #    """
    #    return {
    #        "upstream": self.upstream,
    #        "available_version": ...,
    #        ... update info ...
    #    }

    @XBlock.handler
    def update_from_upstream(self, request=None, suffix=None):
        user_id = requester.user.id if request and request.user else 0
        self._sync_with_upstream(user_id=user_id, apply_updates=True)
        self.save()

    def save(self, *args, **kwargs):
        """
        @@TODO
        """
        for field_name, value in self.upstream_settings.items():
            if field_name not in self.upstream_overridden:
                if value != getattr(self, field_name):
                    self.upstream_overridden.append(field_name)
        super().save()


from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locator import LibraryUsageLocatorV2


def is_block_valid_upstream(usage_key: UsageKey) -> bool:
    """
    @@TODO move
    """
    return isinstance(usage_key, LibraryUsageLocatorV2)
