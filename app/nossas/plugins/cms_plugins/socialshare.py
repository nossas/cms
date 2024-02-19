from cms.api import add_plugin

from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from nossas.design.cms_plugins import UICMSPluginBase

from ..models.socialsharemodel import SocialSharePluginModel
from ..forms.socialshareform import SocialSharePluginForm

@plugin_pool.register_plugin
class SocialSharePlugin(UICMSPluginBase):
    module = "NOSSAS"
    name = _("Social Share Plugin")
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
                "link_context": obj.attributes.get("color").replace("bg-", ""),
                "link_type": "btn",
                "name": "Fazer Download do Documento",
                # "attributes": {
                #     "class": obj.attributes.get("background").replace("bg-", "text-")
                # },
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
