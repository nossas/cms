from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.socialsharemodel import SocialSharePluginModel

@plugin_pool.register_plugin
class SocialSharePlugin(CMSPluginBase):
    model = SocialSharePluginModel
    module = _("Social")
    name = _("Social Share Plugin")
    render_template = "nossas/plugins/social_share.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context
