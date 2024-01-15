from cms.api import add_plugin

# from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.plugins.models.gridmodel import Grid, Column

@plugin_pool.register_plugin
class BootstrapGridPlugin(CMSPluginBase):
    name = "Grid"
    module = "NOSSAS"
    model = Grid
    render_template = "nossas/plugins/grid.html"
    allow_children = True
    child_classes = [
        "BootstrapColumnPlugin"
    ]

    def add_column(self, obj):
        placeholder = obj.placeholder
        language = obj.language
        plugin_type = "BootstrapColumnPlugin"

        obj = add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
        )


    def save_model(self, request, obj, form, change):
        """Change save_model to create plugins by layout"""
        super().save_model(request, obj, form, change)

        if not change:
            for _ in range(3):
                self.add_column(obj)


@plugin_pool.register_plugin
class BootstrapColumnPlugin(CMSPluginBase):
    name = "Coluna"
    module = "NOSSAS"
    model = Column
    render_template = "nossas/plugins/column.html"
    allow_children = True

    def render(self, context, instance, placeholder):
        parent_instance = instance.parent.get_plugin_instance()[0]
        context['parent_instance'] = parent_instance
        return super().render(context, instance, placeholder)
