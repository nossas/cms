from django import forms

from nossas.design.forms import UIBackgroundFormMixin

from nossas.plugins.models.slidermodel import FullPageSlider


class FullPageSliderPluginForm(UIBackgroundFormMixin, forms.ModelForm):
    class Meta:
        model = FullPageSlider
        entangled_fields = {"attributes": []}
        untangled_fields = ["background_image"]
