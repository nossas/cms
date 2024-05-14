from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Accordion, AccordionItem


@plugin_pool.register_plugin
class AccordionPlugin(CMSPluginBase):
    name = "Acordeão"
    model = Accordion
    render_template = "accordion/plugins/accordion.html"
    allow_children = True
    child_classes = ["AccordionItemPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        is_grid = instance.grid_columns > 0

        css_styles = []
        if is_grid:
            css_styles.append(f"--bs-columns:{instance.grid_columns};")

        if instance.bg_color:
            css_styles.append(f"--bs-body-bg:{instance.bg_color};")

        if instance.text_color:
            css_styles.append(f"--bs-body-color:{instance.text_color};")

        context["is_grid"] = is_grid
        context["css_styles"] = "".join(css_styles)

        return context


@plugin_pool.register_plugin
class AccordionItemPlugin(CMSPluginBase):
    name = "Acordeão Item"
    model = AccordionItem
    render_template = "accordion/plugins/accordion_item.html"
    allow_children = True
    require_parent = True
    parent_classes = ["AccordionPlugin"]
