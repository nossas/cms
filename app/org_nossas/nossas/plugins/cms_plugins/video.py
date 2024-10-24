from django import forms
from django.utils.translation import gettext_lazy as _
from cms.plugin_pool import plugin_pool
from djangocms_video.cms_plugins import VideoPlayerPlugin as BaseVideoPlayerPlugin
from djangocms_video.forms import VideoPlayerPluginForm as BaseVideoPlayerPluginForm

from org_nossas.nossas.design.cms_plugins import UICMSPluginBase


plugin_pool.unregister_plugin(BaseVideoPlayerPlugin)


class VideoPlayerPluginForm(BaseVideoPlayerPluginForm):
    label = forms.CharField(
        label=_("Descrição"),
        widget=forms.Textarea(),
        required=False
    )

    embed_link = forms.CharField(
        required=False,
        help_text=_(
            'Utilize este campo para incorporar vídeos de serviços externos como YouTube, Vimeo ou outros. Deixe em branco para fazer upload de arquivos de vídeo adicionando plug-ins de "Source" aninhados.'
        ),
    )


@plugin_pool.register_plugin
class VideoPlayerPlugin(BaseVideoPlayerPlugin, UICMSPluginBase):
    name = _("Video player")
    text_enabled = False
    form = VideoPlayerPluginForm
    fieldsets = [
        (None, {"fields": ("embed_link", "label")}),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "poster",
                    "attributes",
                ),
            },
        ),
    ]
