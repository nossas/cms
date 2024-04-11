from cms.api import add_plugin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import GridForm
from .models import Grid, Column


@plugin_pool.register_plugin
class GridPlugin(CMSPluginBase):
    name = "Grid"
    model = Grid
    render_template = "grid/plugins/grid.html"
    allow_children = True
    child_classes = ["ColumnPlugin"]

    def render(self, context, instance, placeholder):
        css_styles = [f"--bs-gap:{instance.gap}rem"]
        css_classes = ["grid"]

        if instance.alignment:
            css_classes.append(f"align-items-{instance.alignment}")

        context["styles"] = ";".join(css_styles)
        context["classes"] = " ".join(css_classes)
        return super().render(context, instance, placeholder)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and form.cleaned_data["columns"]:
            columns = form.cleaned_data["columns"]

            for x in range(columns):
                add_plugin(
                    placeholder=obj.placeholder,
                    language="pt-br",
                    plugin_type="ColumnPlugin",
                    target=obj,
                    span=12 / columns,
                    span_mobile=12,
                )

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not obj:
            return GridForm

        return super().get_form(request, obj, change, **kwargs)


@plugin_pool.register_plugin
class ColumnPlugin(CMSPluginBase):
    name = "Coluna"
    model = Column
    render_template = "grid/plugins/column.html"
    allow_children = True
    parent_classes = ["GridPlugin", "BlockPlugin"]

    def render(self, context, instance, placeholder):
        css_classes = []
        css_classes.append(f"g-col-{instance.span_mobile}")
        css_classes.append(f"g-col-md-{instance.span}")

        css_styles = []
        if instance.start:
            css_classes.append(f"g-start-md-{instance.start}")

        context["classes"] = " ".join(css_classes)
        if len(css_styles) > 0:
            context["styles"] = ";".join(css_styles)

        return super().render(context, instance, placeholder)
