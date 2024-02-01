from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models.cardmodel import Card


class CreateCardPluginForm(forms.ModelForm):
    title = forms.CharField(label=_("Título"))
    description = forms.CharField(label=_("Descrição"), widget=forms.Textarea, required=False)

    class Meta:
        model = Card
        fields = ["image", "tag", "title", "description"]
