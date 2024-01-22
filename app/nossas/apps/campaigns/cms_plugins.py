# import operator
# from django.contrib import admin
# from django.db.models import Q
# from functools import reduce

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Campaign  # , CampaignListPluginModel, QueryCampaignList


# class QueryCampaignListInline(admin.StackedInline):
#     model = QueryCampaignList
#     extra = 1


@plugin_pool.register_plugin
class CampaignListPlugin(CMSPluginBase):
    name = "Listagem de Campanhas"
    module = "NOSSAS"
    # model = CampaignListPluginModel
    # inlines = [
    #     QueryCampaignListInline,
    # ]
    render_template = "plugins/filter_campaign_list_plugin.html"

    # def get_filter_list(self, instance, qs):
    #     queryfilters = list(
    #         map(lambda x: Q(**x.get_qs_filter()), instance.queries.all())
    #     )

    #     if len(queryfilters) > 0:
    #         return qs.filter(reduce(operator.or_, queryfilters))

    #     return qs

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
