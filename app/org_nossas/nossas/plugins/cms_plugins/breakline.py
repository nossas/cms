from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class BreaklinePlugin(CMSPluginBase):
    name = "Linha"
    module = "NOSSAS"
    text_enabled = True
    render_template = "nossas/plugins/breakline.html"