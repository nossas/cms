from django.utils.translation import gettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class PublicationsApphook(CMSApp):
    app_name = "publications"
    name = _("Publicações")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["nossas.publications.urls"]