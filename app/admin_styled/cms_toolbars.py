from django.utils.translation import gettext_lazy as _
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.conf import get_cms_setting
from cms.cms_toolbars import (
    BasicToolbar,
    # DEFAULT_HELP_MENU_ITEMS,
    HELP_MENU_IDENTIFIER,
    HELP_MENU_BREAK,
)

DEFAULT_HELP_MENU_ITEMS = (
    ("Guia do usuário", "https://nossas.github.io/cms/"),
    # (gettext("Getting started developer guide"), 'https://docs.django-cms.org/en/latest/introduction/index.html'),
    # (gettext("Documentation"), 'https://docs.django-cms.org/en/latest/'),
    # (gettext("User guide"), 'https://docs.google.com/document/d/1f5eWyD_sxUSok436fSqDI0NHcpQ88CXQoDoQm9ZXb0s/'),
    # (gettext("Support Forum"), 'https://discourse.django-cms.org/'),
    # (gettext("Support Slack"), 'https://www.django-cms.org/slack'),
    # (gettext("What's new"), 'https://www.django-cms.org/en/blog/'),
)


@toolbar_pool.register
class ManipulativeToolbar(BasicToolbar):

    def add_help_menu(self):
        """Adds the help menu if it's enabled in settings"""
        if get_cms_setting("ENABLE_HELP"):
            self._help_menu = self.toolbar.get_or_create_menu(
                HELP_MENU_IDENTIFIER, _("Help"), position=-1
            )
            self._help_menu.items = []  # reset the items so we don't duplicate
            for label, url in DEFAULT_HELP_MENU_ITEMS:
                self._help_menu.add_link_item(label, url=url)

            extra_menu_items = get_cms_setting("EXTRA_HELP_MENU_ITEMS")
            if extra_menu_items:
                self._help_menu.add_break(HELP_MENU_BREAK)
                for label, url in extra_menu_items:
                    self._help_menu.add_link_item(label, url=url)


toolbar_pool.unregister(BasicToolbar)
