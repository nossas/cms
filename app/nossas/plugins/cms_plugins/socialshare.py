from cms.api import add_plugin

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from django.utils.translation import gettext_lazy as _

from ..models.socialsharemodel import SocialSharePluginModel
from ..forms.socialshareform import SocialSharePluginForm

@plugin_pool.register_plugin
class SocialSharePlugin(CMSPluginBase):
    module = "NOSSAS"
    name = _("Compartilhamento em Rede Sociais")
    model = SocialSharePluginModel
    form = SocialSharePluginForm
    render_template = "nossas/plugins/social_share.html"
    allow_children = True
    child_classes = ["LinkButtonPlugin"]

    def create_social_share(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        # Child plugins

        # Adiciona link dentro do editor de texto
        plugin_type = "LinkButtonPlugin"
        child_attrs = {
            "config": {
                "link_outline": False,
                "link_context": "branco-nossas",
                "link_type": "btn",
                "name": "Call to Action",
                "external_link": "https://nossas.org"
            }
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

    def save_model(self, request, obj, form, change):
        """Change save_model to create plugins by layout"""
        super().save_model(request, obj, form, change)

        if not change:
            self.create_social_share(obj)

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'selected_social_media': instance.get_selected_social_media_list(),
        })
        return context