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
        context["styles"] = (
            f"--bs-gap:{instance.gap}rem;"
        )

        return super().render(context, instance, placeholder)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and form.cleaned_data['columns']:
            columns = form.cleaned_data['columns']

            for x in range(columns):
                add_plugin(
                    placeholder=obj.placeholder,
                    language='pt-br',
                    plugin_type="ColumnPlugin",
                    target=obj,
                    span=12/columns,
                    span_mobile=12
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
    parent_classes = ["GridPlugin"]

    def render(self, context, instance, placeholder):
        parent_instance = instance.parent.get_plugin_instance()[0]

        context["classes"] = f"g-col-{instance.span_mobile} g-col-md-{instance.span}"

        return super().render(context, instance, placeholder)
