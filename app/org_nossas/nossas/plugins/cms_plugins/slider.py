from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from org_nossas.nossas.design.cms_plugins import UICMSPluginBase
from org_nossas.nossas.plugins.models.slidermodel import FullPageSlider
from org_nossas.nossas.plugins.forms.sliderform import FullPageSliderPluginForm


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
    child_classes = settings.NOSSAS_CONTENT_PLUGINS


@plugin_pool.register_plugin
class FullPageSliderContentPlugin(UICMSPluginBase):
    name = "Página / Slide"
    module = "NOSSAS"
    render_template = "nossas/plugins/full_page_slider_content.html"
    model = FullPageSlider
    form = FullPageSliderPluginForm
    allow_children = True
    child_classes = settings.NOSSAS_CONTENT_PLUGINS
    fields = (
        "background",
        "background_image",
        "x_and_y_center",
        "background_size",
    )

    def render(self, context, instance, placeholder):
        ctx = super().render(context, instance, placeholder)

        if instance.background_image:
            styles = {
                "background-image": f"url('{instance.background_image.url}')",
                "background-size": instance.background_size,
                "background-repeat": "no-repeat",
                "background-position": "center",
            }

            ctx["style"] = ";".join(
                map(lambda key: f"{key}:{styles[key]}", styles.keys())
            )

        return ctx
