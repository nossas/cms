from typing import Any, Dict
from django import forms
from django.core import serializers
from django.forms.models import model_to_dict

from contrib.bonde.models import Community, Mobilization
from contrib.bonde.widgets import (
    CampaignSelectWidget,
    CampaignChoices,
    GroupSelectWidget,
    GroupChoices,
)

from .models import Campaign, Group


class MigrateGroupForm(forms.ModelForm):
    reference_json = forms.ChoiceField(
        label="Objeto de referência",
        help_text="Pesquise pelo nome ou id da comunidade",
        widget=GroupSelectWidget,
    )

    class Meta:
        model = Group
        fields = [
            "reference_json",
        ]

    def __init__(self, *args, **kwargs):
        super(MigrateGroupForm, self).__init__(*args, **kwargs)

        self.fields["reference_json"].choices = GroupChoices()

    def clean_reference_json(self):
        reference_id = self.cleaned_data.get("reference_json")

        if reference_id:
            obj = Community.objects.get(id=int(reference_id))
            return model_to_dict(
                obj, fields=["name", "id", "city", "image", "an_group_id"]
            )

        return reference_id


class ChangeGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "reference_json"]


class MigrateCampaignForm(forms.ModelForm):
    settings = forms.ChoiceField(
        label="Procure por uma mobilização existente",
        help_text="Cria campanha a partir de uma mobilização do Bonde",
        widget=CampaignSelectWidget,
    )
    name = forms.CharField(
        label="ou crie uma nova campanha",
        help_text="Cria uma campanha a partir do CMS",
        required=False,
    )

    class Meta:
        model = Campaign
        fields = ["settings", "name", "slug", "owner_group"]

    def __init__(self, *args, **kwargs):
        super(MigrateCampaignForm, self).__init__(*args, **kwargs)

        self.fields["settings"].choices = CampaignChoices()
        self.fields["slug"].required = False
        self.fields["owner_group"].required = False

    def clean_settings(self):
        reference_id = self.cleaned_data.get("settings")

        if reference_id:
            obj = Mobilization.objects.get(id=int(reference_id))
            return model_to_dict(
                obj,
                fields=[
                    "id",
                    "slug",
                    "name",
                    "goal",
                    "favicon",
                    "custom_domain",
                    "community",
                ],
            )

        return reference_id

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super(MigrateCampaignForm, self).clean()
        settings = cleaned_data.get("settings")
        name = cleaned_data.get("name")
        slug = cleaned_data.get("slug")
        owner_group = cleaned_data.get("owner_group")

        if settings and not name:
            cleaned_data.update(
                {"name": settings.get("name"), "slug": settings.get("slug")}
            )

        if settings and not owner_group:
            group = Group.objects.filter(
                reference_json__id=settings.get("community")
            ).first()

            cleaned_data.update({"owner_group": group})

        required = "Esse campo é obrigatório"
        if not settings and not name:
            self.add_error("name", required)
        if not settings and not slug:
            self.add_error("slug", required)
        if not settings and not owner_group:
            self.add_error("owner_group", required)

        return cleaned_data


class ChangeCampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = "__all__"
