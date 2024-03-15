from django.utils.translation import gettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class TimelineApphook(CMSApp):
    app_name = "timeline"
    name = _("Linha do Tempo")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["nossas.apps.urls.timeline"]
