from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class Tipografia(CMSPluginBase):
    module = "Storybook"
    render_template = "storybook/tipografia.html"