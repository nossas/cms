from django import forms

from nossas.design.forms import UIPaddingFormMixin, UIBackgroundFormMixin

from nossas.plugins.models.buttonmodel import Button


class ButtonPluginForm(UIPaddingFormMixin, UIBackgroundFormMixin, forms.ModelForm):
    class Meta:
        model = Button
        entangled_fields = {"attributes": []}
