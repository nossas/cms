from django import forms

from nossas.design.forms import ( 
    UIBackgroundFormMixin
)

from nossas.plugins.models.headermodel import Header


class HeaderPluginForm(
     UIBackgroundFormMixin, forms.ModelForm
):
    class Meta:
        model = Header
        entangled_fields = {"attributes": []}
