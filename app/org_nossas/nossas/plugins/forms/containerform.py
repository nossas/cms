from django import forms

from org_nossas.nossas.design.forms import (
    UIBackgroundFormMixin,
    UIPaddingFormMixin,
    UIBorderFormMixin,
)

from org_nossas.nossas.plugins.models.containermodel import Container


class ContainerPluginForm(
    UIBackgroundFormMixin, UIPaddingFormMixin, UIBorderFormMixin, forms.ModelForm
):
    class Meta:
        model = Container
        entangled_fields = {"attributes": []}
        untangled_fields = ["fluid"]
