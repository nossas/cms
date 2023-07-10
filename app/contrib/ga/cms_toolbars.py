from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER
from cms.utils.urlutils import add_url_parameters, admin_reverse


@toolbar_pool.register
class GoogleAnalyticsToolbar(CMSToolbar):

    def populate(self):
        self.site = self.request.current_site


        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER, self.current_site.name
        )

        admin_menu.add_sideframe_item(
            "Editar",
            url=admin_reverse("sites_site_change", args=[self.site.id]),
            position=0
        )
