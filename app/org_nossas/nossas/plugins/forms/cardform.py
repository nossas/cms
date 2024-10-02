from django import forms
from django.utils.translation import gettext_lazy as _

# from cms.forms.fields import PageSelectFormField as PageSearchField
from org_nossas.nossas.design.fields import Select2PageSearchField

from ..models.cardmodel import Card


class CardPluginForm(forms.ModelForm):
    internal_link = Select2PageSearchField(
        label=_('Link interno'),
        required=False,
    )

    class Meta:
        model = Card
        fields = ["image", "tag", "internal_link", "external_link", "target"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from cms.models import Page
        self.fields['internal_link'].queryset = Page.objects.drafts().on_site()


class CreateCardPluginForm(CardPluginForm):
    title = forms.CharField(label=_("Título"))
    description = forms.CharField(label=_("Descrição"), widget=forms.Textarea, required=False)

    class Meta:
        model = Card
        fields = ["image", "tag", "title", "description", "internal_link", "external_link", "target"]
