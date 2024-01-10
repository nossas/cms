from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UICMSPluginBase
from nossas.plugins.models.slidermodel import FullPageSlider
from nossas.plugins.forms.sliderform import FullPageSliderPluginForm


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
    render_template = "nossas/plugins/slider_content.html"
    allow_children = True
    require_parent = True
    parent_classes = ["SliderPlugin"]


@plugin_pool.register_plugin
class FullPageSliderContentPlugin(UICMSPluginBase):
    name = "Página / Slide"
    module = "NOSSAS"
    render_template = "nossas/plugins/full_page_slider_content.html"
    model = FullPageSlider
    form = FullPageSliderPluginForm
    allow_children = True
