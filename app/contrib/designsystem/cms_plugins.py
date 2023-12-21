from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


class DSCardPlugin(CMSPluginBase):
    render_template = "ds/plugins/card.html"

plugin_pool.register_plugin(DSCardPlugin)


class DSHeadingPlugin(CMSPluginBase):
    render_template = "ds/plugins/heading.html"

plugin_pool.register_plugin(DSHeadingPlugin)


class DSBreaklinePlugin(CMSPluginBase):
    render_template = "ds/plugins/breakline.html"

plugin_pool.register_plugin(DSBreaklinePlugin)