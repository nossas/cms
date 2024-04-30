from importlib import import_module
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import BlockForm, BlockTemplateForm
from .models import Block, BlockLayout
from .utils import to_padding_css, template_plugin_generator


@plugin_pool.register_plugin
class BlockPlugin(CMSPluginBase):
    name = "Bloco"
    model = Block
    allow_children = True
    change_form_template = "blocks/plugin/change_form.html"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "attributes",
                    "template",
                )
            },
        ),
        (
            _("Estrutura"),
            {"fields": (("element", "layout", "is_container"),)},
        ),
        (
            None,
            {
                "fields": (
                    (
                        "background_color",
                        "padding_top",
                        "padding_bottom",
                        "padding_left",
                        "padding_right",
                    ),
                )
            },
        ),
        (
            _("Atributos"),
            {"fields": ("size", "gap", "alignment", "direction", "wrap", "fill")},
        ),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not change and (not obj or not obj.parent):
            return BlockTemplateForm

        return BlockForm

    def get_render_template(self, context, instance, placeholder):
        """Container styles parent HTML element"""
        if instance.is_container:
            return "blocks/container_plugin.html"

        return "blocks/block_plugin.html"

    def render(self, context, instance, placeholder):
        html_element = instance.element
        block_layout = instance.layout
        css_classes = []
        css_styles = []

        if instance.is_container:
            container_size = (
                instance.attributes.get("size", None) if instance.attributes else None
            )
            if container_size:
                css_classes.append(f"container-{container_size}")
            else:
                css_classes.append("container")

        if block_layout == BlockLayout.grid or block_layout == BlockLayout.flex:
            css_classes.append(block_layout)

            if instance.attributes and instance.attributes.get("gap"):
                gap = instance.attributes.get("gap")
                css_styles.append(f"--bs-gap:{gap}rem")

            if instance.attributes and instance.attributes.get("alignment"):
                alignment = instance.attributes.get("alignment")
                css_classes.append(f"align-items-{alignment}")

        if block_layout == BlockLayout.flex:
            if instance.attributes and instance.attributes.get("direction"):
                direction = instance.attributes.get("direction")

                if direction == "row":
                    css_classes.append("flex-column")
                    css_classes.append(f"flex-md-row")
                elif direction == "row-reverse":
                    css_classes.append("flex-column-reverse")
                    css_classes.append(f"flex-md-row-reverse")
                else:
                    css_classes.append(f"flex-{direction}")
            else:
                css_classes.append("flex-column")
                css_classes.append("flex-md-row")

            if instance.attributes and instance.attributes.get("wrap"):
                wrap = instance.attributes.get("wrap")
                css_classes.append(f"flex-{wrap}")

            if instance.attributes and instance.attributes.get("fill"):
                css_classes.append(f"d-flex-fill")

        background_color = (
            instance.attributes.get("background_color", None)
            if instance.attributes
            else None
        )
        if background_color:
            css_styles.append(f"background-color:{background_color}")

        padding_attrs = [("padding_top", "pt"), ("padding_bottom", "pb"), ("padding_left", "pl"), ("padding_right", "pr")]

        for key, attr in padding_attrs:
            p = instance.attributes.get(key, None) if instance.attributes else None
            if p:
                css_classes.append(f"{attr}-{p}")


        context["html_element"] = html_element
        context["css_classes"] = " ".join(css_classes)
        context["css_styles"] = ";".join(css_styles)

        return super().render(context, instance, placeholder)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and form.cleaned_data["template"]:
            module_template = import_module(
                f"contrib.ds.blocks.schemas.{form.cleaned_data['template']}"
            )

            all(template_plugin_generator(obj, module_template.schema))
