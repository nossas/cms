from django.utils.translation import gettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class CampaignsApphook(CMSApp):
    app_name = "campaigns"
    name = _("Campanhas")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["org_nossas.nossas.apps.urls.campaigns"]
