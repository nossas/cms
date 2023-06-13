from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import AddBlockForm
from .models import (
    Block,
    Button,
    Grid,
    Navbar,
    SocialMedia,
    SocialMediaItem,
    Partners,
    PartnersItem,
)
from .utils import copy_by_layout


@plugin_pool.register_plugin
class BlockPlugin(CMSPluginBase):
    model = Block
    name = "Bloco"
    module = "Frontend"
    render_template = "frontend/plugins/block.html"
    allow_children = True
    child_classes = ["PicturePlugin", "TextPlugin", "GridPlugin", "ButtonPlugin"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (
            None,
            {"fields": [("title", "slug"), ("spacing", "alignment")]},
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

    def get_form(self, request, obj, change, **kwargs):
        if not change:
            self.form = AddBlockForm
        
        return super(BlockPlugin, self).get_form(request, obj, change, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(BlockPlugin, self).get_fieldsets(request, obj)

        if not obj:
            fieldsets[0] = (
                None,
                {"fields": [("title", "slug"), ("spacing", "layout")]},
            )
        else:
            fieldsets[0] = (
                None,
                {"fields": [("title", "slug"), ("spacing", "alignment")]},
            )

        return fieldsets

    def save_model(self, request, obj, form, change):
        super(BlockPlugin, self).save_model(request, obj, form, change)

        if not change:
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
        "TextPlugin",
        "ButtonPlugin",
        "SocialMediaPlugin",
        "PartnersPlugin",
        "PressurePlugin"
    ]

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
            plugins = placeholder.get_child_plugins().filter(plugin_type="BlockPlugin").order_by("position")

            context["children"] = list(
                filter(
                    lambda x: not x.menu_hidden and not x.hidden,
                    map(lambda x: x.get_bound_plugin(), plugins),
                )
            )
        else:
            context["children"] = list()

        return context


@plugin_pool.register_plugin
class ButtonPlugin(CMSPluginBase):
    name = "Button"
    module = "Frontend"
    model = Button
    render_template = "frontend/plugins/button.html"
    fieldsets = [
        (None, {"fields": ["title", ("action_url", "target_blank")]}),
        ("Estilo", {"fields": [("font", "color"), ("background_color", "bold")]}),
        (
            "Borda",
            {
                "classes": ["collapse"],
                "fields": ["border_color", "border_size", "rounded"],
            },
        ),
    ]


class SocialMediaItemInline(admin.TabularInline):
    model = SocialMediaItem


@plugin_pool.register_plugin
class SocialMediaPlugin(CMSPluginBase):
    name = "Social Media"
    module = "Frontend"
    render_template = "frontend/plugins/social-media.html"
    model = SocialMedia
    inlines = [SocialMediaItemInline]


class PartnersItemInline(admin.TabularInline):
    model = PartnersItem


@plugin_pool.register_plugin
class PartnersPlugin(CMSPluginBase):
    name = "Partners"
    module = "Frontend"
    render_template = "frontend/plugins/partners.html"
    model = Partners
    inlines = [PartnersItemInline]
