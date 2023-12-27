from django import forms

from nossas.design.forms import UIPaddingFormMixin, UIBackgroundFormMixin

from nossas.plugins.models.boxmodel import Box


class BoxPluginForm(UIPaddingFormMixin, UIBackgroundFormMixin, forms.ModelForm):
    class Meta:
        model = Box
        entangled_fields = {"attributes": []}
