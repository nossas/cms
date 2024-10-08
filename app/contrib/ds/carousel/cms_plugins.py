from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Carousel, CarouselContent


@plugin_pool.register_plugin
class CarouselPlugin(CMSPluginBase):
    name = "Carrossel"
    model = Carousel
    render_template = "carousel/plugins/carousel.html"
    allow_children = True
    child_classes = ["CarouselContentPlugin"]

    def render(self, context, instance, placeholder):
        context["indicators"] = range(instance.num_children())
        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class CarouselContentPlugin(CMSPluginBase):
    name = "Carrosel Item"
    model = CarouselContent
    render_template = "carousel/plugins/carousel_content.html"
    allow_children = True
    parent_classes = ["CarouselPlugin"]

    def render(self, context, instance, placeholder):
        context["is_active"] = instance.position == 0
        return super().render(context, instance, placeholder)
