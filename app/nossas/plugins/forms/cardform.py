from django import forms

from ..models.cardmodel import Card


class CreateCardPluginForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Card
        fields = ["image", "tag", "title", "description"]
