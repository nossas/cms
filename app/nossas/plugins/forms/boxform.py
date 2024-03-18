from django import forms
from django.db.models import TextChoices

from nossas.design.forms import UIBackgroundFormMixin, CORES_TEMAS, UIBackgroundSelect

from nossas.plugins.models.boxmodel import Box


class BoxLayoutChoices(TextChoices):
    cta = "cta", "CTA"
    share = "share", "Compartilhar nas redes sociais"


class BoxPluginForm(UIBackgroundFormMixin, forms.ModelForm):
    color = forms.ChoiceField(
        choices=CORES_TEMAS, required=False, widget=UIBackgroundSelect()
    )

    class Meta:
        model = Box
        entangled_fields = {"attributes": ["color"]}


class LayoutBoxPluginForm(BoxPluginForm):
    layout = forms.ChoiceField(
        choices=BoxLayoutChoices.choices, initial=BoxLayoutChoices.cta, required=False
    )
    class Meta:
        model = Box
        entangled_fields = {"attributes": []}
        untangled_fields = ["layout"]
