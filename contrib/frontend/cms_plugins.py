from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    Button,
    SocialMedia,
    SocialMediaItem,
    Partners,
    PartnersItem,
)


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
    fields = ("url", "kind", "picture", )


@plugin_pool.register_plugin
class SocialMediaPlugin(CMSPluginBase):
    name = "Social Media"
    module = "Frontend"
    render_template = "frontend/plugins/social-media.html"
    model = SocialMedia
    inlines = [SocialMediaItemInline]


class PartnersItemInline(admin.TabularInline):
    model = PartnersItem
    fields = ["picture", "url"]


@plugin_pool.register_plugin
class PartnersPlugin(CMSPluginBase):
    name = "Partners"
    module = "Frontend"
    render_template = "frontend/plugins/partners.html"
    model = Partners
    inlines = [PartnersItemInline]
