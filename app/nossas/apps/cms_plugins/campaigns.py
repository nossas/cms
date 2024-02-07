from django.core.paginator import Paginator

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.campaigns import Campaign
from ..forms.campaigns import CampaignFilterForm


@plugin_pool.register_plugin
class CampaignListPlugin(CMSPluginBase):
    name = "Listagem de Campanhas"
    module = "NOSSAS"
    render_template = "plugins/filter_campaign_list_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        params = context["request"].GET

        form = CampaignFilterForm()
        queryset = Campaign.on_site.filter(hide=False)

        if len(params.keys()) > 0:
            form = CampaignFilterForm(data=params)

            if form.is_valid():
                filters = {}
                release_year = form.cleaned_data.get("release_year")
                if release_year:
                    filters["release_date__year"] = release_year

                tags = form.cleaned_data.get("tags")
                if tags:
                    filters["tags__slug__in"] = tags

                campaign_group_id = form.cleaned_data.get("campaign_group_id")
                if campaign_group_id:
                    filters["campaign_group__id"] = campaign_group_id

                queryset = queryset.filter(**filters)

        paginator = Paginator(queryset, 10)
        page = paginator.page(context["request"].GET.get("page", 1))

        context.update(
            {
                "campaign_list": page.object_list,
                "paginator": paginator,
                "page": page,
                "form": form,
            }
        )

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
