from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Block, Grid, ColumnChoices, LayoutChoices
from .utils import copy_by_layout


@plugin_pool.register_plugin
class BlockPlugin(CMSPluginBase):
    model = Block
    name = "Bloco"
    module = "Frontend"
    render_template = "frontend/plugins/block.html"
    allow_children = True
    child_classes = [
        "PicturePlugin",
        "TextPlugin",
        "GridPlugin"
        # "ActionButtonPlugin",
        # "RowPlugin",
    ]
    prepopulated_fields = {"slug": ("title", )}
    fieldsets = [
        (
            None,
            {
                "fields": [("title", "slug"), "layout", "spacing"]
            },
        ),
        (
            "Background",
            {
                "fields": [("background_color", "background_image")]
            }
        ),
        (
            "Opções avançadas",
            {
                "classes": ["collapse"],
                "fields": ["menu_title", "menu_hidden", "hidden"]
            }
        )
    ]

    def save_model(self, request, obj, form, change):
        super(BlockPlugin, self).save_model(request, obj, form, change)

        copy_by_layout(obj=obj, layout=form.cleaned_data["layout"])



@plugin_pool.register_plugin
class GridPlugin(CMSPluginBase):
    name = "Grid"
    module = "Frontend"
    model = Grid
    render_template = "frontend/plugins/grid.html"
    allow_children = True
    child_classes = [
        "ColumnPlugin",
    ]


@plugin_pool.register_plugin
class ColumnPlugin(CMSPluginBase):
    name = "Coluna"
    module = "Frontend"
    render_template = "frontend/plugins/column.html"
    allow_children = True
    child_classes = [
        "PicturePlugin",
        "TextPlugin"
    ]

    def render(self, context, instance, placeholder):
        context = super(ColumnPlugin, self).render(context, instance, placeholder)

        parent_instance, plugin_class = instance.parent.get_plugin_instance()

        context['alignment'] = parent_instance.align

        return context