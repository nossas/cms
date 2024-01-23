from django import forms

from nossas.design.forms import (
    UIBackgroundFormMixin,
    UIPaddingFormMixin,
    UIBorderFormMixin,
)

from nossas.plugins.models.containermodel import Container


class ContainerPluginForm(
    UIBackgroundFormMixin, UIPaddingFormMixin, UIBorderFormMixin, forms.ModelForm
):
    class Meta:
        model = Container
        entangled_fields = {"attributes": []}
