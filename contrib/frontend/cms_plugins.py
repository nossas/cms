from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Block, Grid, Navbar
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
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (
            None,
            {"fields": [("title", "slug"), "layout", "spacing"]},
        ),
        ("Background", {"fields": [("background_color", "background_image")]}),
        (
            "Opções avançadas",
            {
                "classes": ["collapse"],
                "fields": ["menu_title", "menu_hidden", "hidden"],
            },
        ),
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
    child_classes = ["PicturePlugin", "TextPlugin"]

    def render(self, context, instance, placeholder):
        context = super(ColumnPlugin, self).render(context, instance, placeholder)

        parent_instance, plugin_class = instance.parent.get_plugin_instance()

        context["alignment"] = parent_instance.align

        return context


@plugin_pool.register_plugin
class NavbarPlugin(CMSPluginBase):
    name = "Navbar"
    module = "Frontend"
    model = Navbar
    render_template = "frontend/plugins/navbar.html"
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(NavbarPlugin, self).render(context, instance, placeholder)

        current_page = context["request"].current_page

        placeholder = current_page.get_placeholders().get(slot="content")

        if placeholder:
            plugins = placeholder.get_child_plugins().filter(plugin_type="BlockPlugin")

            context["children"] = list(
                filter(
                    lambda x: not x.menu_hidden and not x.hidden,
                    map(lambda x: x.get_bound_plugin(), plugins),
                )
            )
        else:
            context["children"] = list()

        return context
