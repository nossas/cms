from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class SiteFooterPlugin(CMSPluginBase):
    name = "Site Footer"
    module = "NOSSAS"
    render_template = "nossas/plugins/site_footer.html"