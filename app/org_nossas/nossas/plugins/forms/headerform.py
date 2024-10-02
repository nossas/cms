from django import forms

from org_nossas.nossas.design.fields import GraphicElementRadioSelect, GraphicIconRadioSelect
from org_nossas.nossas.design.forms import UIBackgroundFormMixin

from org_nossas.nossas.plugins.models.headermodel import Header, HeaderImage


class HeaderPluginForm(UIBackgroundFormMixin, forms.ModelForm):
    class Meta:
        model = Header
        entangled_fields = {"attributes": []}
        untangled_fields = ["graphic_element"]
        widgets = {"graphic_element": GraphicElementRadioSelect}



class HeaderImagePluginForm(forms.ModelForm):
    class Meta:
        model = HeaderImage
        fields = ["picture", "graphic_icon"]
        widgets = {"graphic_icon": GraphicIconRadioSelect}