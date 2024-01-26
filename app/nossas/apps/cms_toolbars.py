from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER
from cms.utils.urlutils import reverse


@toolbar_pool.register
class InstitutionalToolbar(CMSToolbar):
    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER, self.current_site.name
        )

        # Create view to redirect add or change admin url based on check request.current_site
        url = reverse("institutional:redirect_add_or_change")

        admin_menu.add_modal_item(
            "Informações",
            url=url,
            position=0,
        )
