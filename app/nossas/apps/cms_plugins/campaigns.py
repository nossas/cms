import re
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.campaigns import Campaign, NavigateCampaigns, OurCitiesProject
from ..forms.campaigns import CampaignFilterForm


@plugin_pool.register_plugin
class CampaignListPlugin(CMSPluginBase):
    name = _("Listagem de Campanhas")
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

                if (
                    settings.DATABASES.get("default").get("ENGINE")
                    == "django.db.backends.sqlite3"
                ):
                    queryset = queryset.filter(**filters)
                else:
                    queryset = queryset.filter(**filters).order_by("id").distinct("id")

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
    name = _("Navegue por Campanhas")
    module = "NOSSAS"
    model = NavigateCampaigns
    render_template = "plugins/navigate_campaigns_plugin.html"
    fields = ("filter_tags", "filter_campaign_group")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context["request"]
        pattern = re.compile(r"/(campanhas|campaigns)/([0-9]+)/")

        campaign_id = pattern.search(request.path_info).group(2)
        campaign = None

        if campaign_id:
            campaign = Campaign.on_site.get(id=campaign_id)
        elif instance.related_campaign:
            campaign = instance.related_campaign

        queryset = Campaign.on_site.filter(hide=False)

        if campaign:
            queryset = queryset.exclude(id=campaign.id)

            if instance.filter_tags:
                queryset = queryset.filter(
                    tags__slug__in=list(map(lambda x: x.slug, campaign.tags.all()))
                )

            if instance.filter_campaign_group:
                queryset = queryset.filter(campaign_group=campaign.campaign_group)

        if (
            settings.DATABASES.get("default").get("ENGINE")
            != "django.db.backends.sqlite3"
        ):
            queryset = queryset.order_by("id").distinct("id")

        context.update({"campaign_list": queryset[:3]})

        return context


@plugin_pool.register_plugin
class OurCitiesProjectPlugin(CMSPluginBase):
    name = _("Projeto Nossas Cidades")
    module = "NOSSAS"
    model = OurCitiesProject
    render_template = "plugins/our_cities_plugin.html"
    allow_children = True
    child_classes = ["TextPlugin"]
    autocomplete_fields = ["related_campaigns"]
