from django import forms

from nossas.design.forms import ( 
    UIBackgroundFormMixin
)

from nossas.plugins.models.containermodel import Container


class ContainerPluginForm(
     UIBackgroundFormMixin, forms.ModelForm
):
    class Meta:
        model = Container
        entangled_fields = {"attributes": []}

