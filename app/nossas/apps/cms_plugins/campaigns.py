from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.campaigns import Campaign


@plugin_pool.register_plugin
class CampaignListPlugin(CMSPluginBase):
    name = "Listagem de Campanhas"
    module = "NOSSAS"
    render_template = "plugins/filter_campaign_list_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update({"campaign_list": Campaign.on_site.filter(hide=False)})

        return context


@plugin_pool.register_plugin
class NavigateCampaignsPlugin(CMSPluginBase):
    name = "Navegue por Campanhas"
    module = "NOSSAS"
    render_template = "plugins/navigate_campaigns_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update({"campaign_list": Campaign.on_site.filter(hide=False)[:3]})

        return context
