"""
Mixin class that provides authoring capabilities for XBlocks.
"""


import logging

from django.conf import settings
from web_fragments.fragment import Fragment
from xblock.core import XBlock, XBlockMixin
from xblock.fields import Integer, String, Scope, Dict

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

    # Note: upstream_* fields are only used by CMS. Not needed in the LMS.
    upstream_block = String(
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
    upstream_block_version = Integer(
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
    upstream_block_settings = Dict(
        scope=Scope.settings,
        help=(
            "@@TODO"
        ),
        hidden=True,
        default={},
        enforce_type=True,
    )
