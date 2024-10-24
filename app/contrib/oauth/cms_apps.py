from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class OAuthApphook(CMSApp):
    app_name = "oauth"  # must match the application namespace
    name = "OAuth"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["contrib.oauth.urls"]