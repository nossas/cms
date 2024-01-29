from django import forms
from django.db.models import TextChoices

from nossas.design.forms import UIBackgroundFormMixin, CORES_TEMAS, UIBackgroundSelect

from nossas.plugins.models.boxmodel import Box


class BoxPluginForm(UIBackgroundFormMixin, forms.ModelForm):
    color = forms.ChoiceField(
        choices=CORES_TEMAS, required=False, widget=UIBackgroundSelect()
    )

    class Meta:
        model = Box
        entangled_fields = {"attributes": ["color"]}
