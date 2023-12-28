from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UIPaddingMixin, UIBackgroundMixin, CMSUIPlugin
from nossas.plugins.models.boxmodel import Box
from nossas.plugins.forms.boxform import BoxPluginForm


@plugin_pool.register_plugin
class SliderPlugin(CMSPluginBase):
    name = "Slider"
    module = "NOSSAS"
    render_template = "nossas/plugins/slider.html"
    allow_children = True
    child_classes = ["SliderContentPlugin"]


@plugin_pool.register_plugin
class SliderContentPlugin(CMSPluginBase):
    name = "Slider Content"
    module = "NOSSAS"
    render_template = "nossas/plugins/slider-content.html"
    allow_children = True
    require_parent = True
    parent_classes = ['SliderPlugin']
