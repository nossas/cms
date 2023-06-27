from django.urls import reverse

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.cms_toolbars import HELP_MENU_IDENTIFIER


@toolbar_pool.register
class OpenAIToolbar(CMSToolbar):

    def populate(self):

        help_menu = self.toolbar.get_menu(HELP_MENU_IDENTIFIER)

        help_menu.add_modal_item(
            name="ChatGPT",
            url=reverse("openai")
        )