from django import forms

from org_nossas.nossas.design.fields import GraphicIconRadioSelect

from ..models.breadcrumbmodel import Breadcrumb


class BreadcrumbPluginForm(forms.ModelForm):
    class Meta:
        model = Breadcrumb
        fields = ["graphic_icon"]
        widgets = {"graphic_icon": GraphicIconRadioSelect}
