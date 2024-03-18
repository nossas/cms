from django import forms
from django.utils.translation import gettext_lazy as _

from cms.models import Page
from nossas.design.fields import Select2PageSearchField

from .models import Publication


class PublicationForm(forms.ModelForm):
    parent = Select2PageSearchField(
        label=_("Página Relacionada"),
        required=False,
    )

    class Meta:
        model = Publication
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["parent"].queryset = Page.objects.drafts().on_site()
