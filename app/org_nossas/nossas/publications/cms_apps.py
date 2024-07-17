from django.utils.translation import gettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class PublicationsApphook(CMSApp):
    app_name = "publications"
    name = _("Publicações")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["org_nossas.nossas.publications.urls"]



@apphook_pool.register
class SearchApphook(CMSApp):
    app_name = "haystack"
    name = _("Buscador")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["org_nossas.nossas.urls_search"]