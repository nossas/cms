from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_picture.cms_plugins import PicturePlugin as DjangoCMSPicturePlugin

from .models import Button


@plugin_pool.register_plugin
class ImagePlugin(DjangoCMSPicturePlugin):
    module = "Frontend"
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "picture",
                    "external_picture",
                    ("width", "height"),
                )
            },
        ),
        (
            _("Link settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("link_url", "link_page"),
                    "link_target",
                    "link_attributes",
                ),
            },
        ),
        (
            _("Cropping settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("use_automatic_scaling", "use_no_cropping"),
                    ("use_crop", "use_upscale"),
                    "thumbnail_options",
                ),
            },
        ),
    ]

   
    def render(self, context, instance, placeholder):
        context = super(ImagePlugin, self).render(context, instance, placeholder)
        current_page = context["request"].current_page 
        if current_page.publisher_is_draft:
            del context["picture_link"]
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
