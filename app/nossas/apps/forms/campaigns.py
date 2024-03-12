from django import forms
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

from django_select2 import forms as s2forms
from tag_fields.models import ModelTag
from ..models.campaigns import CampaignGroup, Campaign, OurCitiesProject


def get_tags():
    return list(ModelTag.objects.values_list("slug", "name"))


def get_campaign_groups():
    return list(CampaignGroup.on_site.values_list("id", "name"))


def get_release_years():
    return list(
        Campaign.on_site.dates("release_date", "year").values_list(
            "release_date__year", "release_date__year"
        )
    )


class CampaignFilterForm(forms.Form):
    tags = forms.MultipleChoiceField(
        label=_("Temática"),
        choices=lazy(get_tags, tuple)(),
        widget=s2forms.Select2MultipleWidget(),
        required=False,
    )
    campaign_group_id = forms.ChoiceField(
        label=_("Cidade"),
        choices=lazy(get_campaign_groups, tuple)(),
        widget=s2forms.Select2MultipleWidget,
        required=False,
    )
    release_year = forms.ChoiceField(
        label=_("Ano"),
        choices=lazy(get_release_years, tuple)(),
        widget=s2forms.Select2MultipleWidget,
        required=False,
    )
