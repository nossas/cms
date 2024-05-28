from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import ButtonForm
from .models import Button, Target, IconPosition


@plugin_pool.register_plugin
class ButtonPlugin(CMSPluginBase):
    name = "Botão"
    model = Button
    form = ButtonForm
    change_form_template = "link/admin/plugin/change_form.html"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "label",
                    ("internal_link", "external_link", "link_target"),
                )
            },
        ),
        (
            "Estilização",
            {
                "fields": (
                    ("context", "styled", "size"),
                    ("icon", "icon_position"),
                )
            },
        ),
    )

    def get_render_template(self, context, instance, placeholder):
        if instance.link_target == Target.submit:
            return "link/plugins/submit.html"

        return "link/plugins/button.html"

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
        
        if instance.icon_position == IconPosition.only:
            css_classes.append("btn-icon")

        context["css_classes"] = " ".join(css_classes)
        # context["css_styles"] = ";".join(css_styles)

        return super().render(context, instance, placeholder)
