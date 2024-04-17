from django import forms

from .fields import Select2PageSearchField
from .models import Button


class ButtonForm(forms.ModelForm):
    internal_link = Select2PageSearchField(
        # label=_('Link interno'),
        required=False,
        # help_text=_('Se fornecido, substitui o link externo.'),
    )

    class Meta:
        model = Button
        fields = "__all__"