from cms.api import add_plugin

from cms.plugin_pool import plugin_pool
from org_nossas.nossas.design.cms_plugins import UICMSPluginBase

from django.utils.translation import gettext_lazy as _

from ..models.socialsharemodel import SocialSharePluginModel
from ..forms.socialshareform import SocialSharePluginForm

@plugin_pool.register_plugin
class SocialSharePlugin(UICMSPluginBase):
    module = "NOSSAS"
    name = _("Compartilhar em Rede Social")
    model = SocialSharePluginModel
    form = SocialSharePluginForm
    render_template = "nossas/plugins/social_share.html"

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'selected_social_media': instance.get_selected_social_media_list(),
        })
        return context
