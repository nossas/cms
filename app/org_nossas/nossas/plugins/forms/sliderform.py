from django import forms

from org_nossas.nossas.design.forms import UIBackgroundFormMixin

from org_nossas.nossas.plugins.models.slidermodel import FullPageSlider


class FullPageSliderPluginForm(UIBackgroundFormMixin, forms.ModelForm):
    class Meta:
        model = FullPageSlider
        entangled_fields = {"attributes": []}
        untangled_fields = ["background_image", "x_and_y_center", "background_size"]
