from cms.api import add_plugin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class GridPlugin(CMSPluginBase):
    name = "Grid"
    # model = Grid
    render_template = "grid/plugins/grid.html"
    allow_children = True
    child_classes = ["ColumnPlugin"]

    def add_column(self, obj):
        placeholder = obj.placeholder
        language = obj.language
        plugin_type = "ColumnPlugin"

        obj = add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
        )

    # def save_model(self, request, obj, form, change):
    #     """Change save_model to create plugins by layout"""
    #     super().save_model(request, obj, form, change)

    #     if not change:
    #         cols = layout_dict.get(obj.grid_layout, 0)

    #         for _ in range(cols):
    #             self.add_column(obj)


@plugin_pool.register_plugin
class ColumnPlugin(CMSPluginBase):
    name = "Coluna"
    # model = Column
    render_template = "grid/plugins/column.html"
    allow_children = True
    parent_classes = ["GridPlugin"]

    # def render(self, context, instance, placeholder):
    #     parent_instance = instance.parent.get_plugin_instance()[0]
    #     context["parent_instance"] = parent_instance
    #     return super().render(context, instance, placeholder)