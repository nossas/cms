from django import forms
from django.db.models import TextChoices

from nossas.design.forms import (
    UIPaddingFormMixin,
    UIBackgroundFormMixin,
    UIBorderFormMixin,
)

from nossas.plugins.models.boxmodel import Box


class BoxLayoutChoices(TextChoices):
    empty = "", "Vazio"
    cta = "cta", "CTA"


class BoxPluginForm(
    UIPaddingFormMixin, UIBackgroundFormMixin, UIBorderFormMixin, forms.ModelForm
):
    class Meta:
        model = Box
        entangled_fields = {"attributes": []}


class LayoutBoxPluginForm(BoxPluginForm):
    layout = forms.ChoiceField(
        choices=BoxLayoutChoices.choices, initial=BoxLayoutChoices.empty, required=False
    )

    class Meta:
        model = Box
        entangled_fields = {"attributes": []}
        untangled_fields = ["layout"]
