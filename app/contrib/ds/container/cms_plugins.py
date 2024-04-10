from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Container


@plugin_pool.register_plugin
class ContainerPlugin(CMSPluginBase):
    name = "Container"
    render_template = "container/plugins/container.html"
    allow_children = True
    model = Container

    def render(self, context, instance, placeholder):
        context["classes"] = "container"

        if instance.size:
            context["classes"] = f"container-{instance.size}"

        return super().render(context, instance, placeholder)