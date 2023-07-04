# from django.contrib import admin
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_picture.cms_plugins import PicturePlugin as DjangoCMSPicturePlugin
from djangocms_video.cms_plugins import VideoPlayerPlugin as DjangoCMSVideoPlayerPlugin
from djangocms_video.models import VideoPlayer

from .models import Button


class ImageForm(forms.ModelForm):
    external_picture = forms.CharField(label=_("External picture"), required=False)

    def clean(self):
        cleaned_data = super(ImageForm, self).clean()

        picture = cleaned_data.get("picture")
        external_picture = cleaned_data.get("external_picture", None)

        protocol = "http://" if settings.DEBUG else "https://"
        domain = Site.objects.get_current().domain

        if (
            picture
            and external_picture
            and (
                external_picture.startswith("/static/")
                or external_picture.startswith(protocol + domain)
            )
        ):
            cleaned_data.update({"external_picture": None})

        elif (
            not picture and external_picture and external_picture.startswith("/static/")
        ):
            external_picture = f"{protocol}{domain}{external_picture}"
            external_picture = external_picture.replace(" ", "_")

            cleaned_data.update({"external_picture": external_picture})

        return cleaned_data


@plugin_pool.register_plugin
class ImagePlugin(DjangoCMSPicturePlugin):
    module = "Frontend"
    form = ImageForm
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

class VideoForm(forms.ModelForm):
    width = forms.IntegerField(label=_("Width"), required=False)
    height = forms.IntegerField(label=_("Height"), required=False)
    class Meta:
        model = VideoPlayer
        fields = "__all__"

@plugin_pool.register_plugin
class VideoPlugin(DjangoCMSVideoPlayerPlugin):
    name = "Video"
    module = "Frontend"
    form = VideoForm
    model = VideoPlayer
    fieldsets = [
        (None, {"fields": ["embed_link", "width", "height"]}),
        
    ]
    def save_model(self, request, obj, form, change):
        width = form.cleaned_data["width"]
        height = form.cleaned_data["height"]
        if width and height:
            obj.attributes = dict(width=width, height=height)
        
        return super(VideoPlugin, self).save_model(request, obj, form, change)
