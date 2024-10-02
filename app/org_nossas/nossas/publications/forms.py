from django import forms
from django.utils.translation import gettext_lazy as _

from cms.models import Page
from org_nossas.nossas.design.fields import Select2PageSearchField

from .models import Publication, PublicationList
from .widgets import Select2CategorySelectWidget


class PublicationForm(forms.ModelForm):
    parent = Select2PageSearchField(
        label=_("Categoria"),
        required=False,
        widget=Select2CategorySelectWidget(),
        help_text=_(
            "Atualmente, apenas as categorias pré-definidas estão disponíveis. Para adicionar uma nova categoria, entre em contato com o administrador do sistema através do canal de suporte."
        ),
    )

    class Meta:
        model = Publication
        fields = "__all__"


class PublicationListForm(forms.ModelForm):
    category = Select2PageSearchField(
        label=_("Categoria"), required=False, widget=Select2CategorySelectWidget()
    )

    class Meta:
        model = PublicationList
        fields = "__all__"
