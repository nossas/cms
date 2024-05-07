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
    change_form_template = "link/admin/plugin/change_form.html"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "label",
                    (
                        "internal_link",
                        "external_link",
                        "link_target"
                    ),
                )
            },
        ),
        (
            "Estilização",
            {
                "fields": (
                    ("context", "styled", "size"),
                )
            },
        ),
    )

    def render(self, context, instance, placeholder):
        css_classes = ["btn"]
        # css_styles = []

        if instance.size:
            css_classes.append(f"btn-{instance.size}")

        styled = "btn"

        if instance.styled:
            styled += f"-{instance.styled}"

        if instance.context:
            styled += f"-{instance.context}"

        if styled != "btn":
            css_classes.append(styled)

        context["css_classes"] = " ".join(css_classes)
        # context["css_styles"] = ";".join(css_styles)

        return super().render(context, instance, placeholder)
