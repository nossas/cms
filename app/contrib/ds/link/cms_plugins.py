from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import ButtonForm
from .models import Button


@plugin_pool.register_plugin
class ButtonPlugin(CMSPluginBase):
    name = "Botão"
    model = Button
    form = ButtonForm
    render_template = "link/plugins/button.html"

    def render(self, context, instance, placeholder):
        css_classes = ["btn"]
        # css_styles = []

        if instance.context:
            css_classes.append(f"btn-{instance.context}")

        context["css_classes"] = " ".join(css_classes)
        # context["css_styles"] = ";".join(css_styles)

        return super().render(context, instance, placeholder)
