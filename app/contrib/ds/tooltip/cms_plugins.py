from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Tooltip


@plugin_pool.register_plugin
class TooltipPlugin(CMSPluginBase):
    name = "Tooltip"
    model = Tooltip
    render_template = "tooltip/plugins/tooltip.html"
    text_enabled = True
    allow_children = True