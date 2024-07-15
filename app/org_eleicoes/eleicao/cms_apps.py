from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class EleicaoApphook(CMSApp):
    app_name = "eleicao"  # must match the application namespace
    name = "Eleição do ano"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["eleicao.urls"]
