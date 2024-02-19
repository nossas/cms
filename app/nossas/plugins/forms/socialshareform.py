from django import forms

from nossas.design.forms import UIBackgroundFormMixin, CORES_TEMAS, UIBackgroundSelect

from nossas.plugins.models.socialsharemodel import SocialSharePluginModel


class SocialSharePluginForm(UIBackgroundFormMixin, forms.ModelForm):
    color = forms.ChoiceField(
        choices=CORES_TEMAS, required=False, widget=UIBackgroundSelect()
    )

    class Meta:
        model = SocialSharePluginModel
        entangled_fields = {"attributes": ["color"]}
