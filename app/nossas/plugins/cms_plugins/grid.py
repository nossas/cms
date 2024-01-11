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