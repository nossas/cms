from django import forms

from nossas.design.forms import (
    UIPaddingFormMixin,
    UIBackgroundFormMixin,
    UIBorderFormMixin,
)

from nossas.plugins.models.boxmodel import Box


class BoxPluginForm(
    UIPaddingFormMixin, UIBackgroundFormMixin, UIBorderFormMixin, forms.ModelForm
):
    class Meta:
        model = Box
        entangled_fields = {"attributes": []}
