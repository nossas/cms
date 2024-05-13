from django import forms
from django.utils.translation import gettext as _

from .fields import Select2PageSearchField
from .models import Button, Target


class ButtonForm(forms.ModelForm):
    internal_link = Select2PageSearchField(
        label=_("Link interno"),
        required=False,
        # help_text=_('Se fornecido, substitui o link externo.'),
    )

    class Meta:
        model = Button
        fields = "__all__"

    class Media:
        js = [
            "ds/link/js/icon-field.js",
            "ds/link/js/preview.js"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["label"].widget.attrs["placeholder"] = _(
            "Digite o texto do botão aqui"
        )
        self.fields["link_target"].widget.initial = Target._self

        self.fields["internal_link"].widget.attrs["placeholder"] = _(
            "Selecione uma página"
        )
        self.fields["external_link"].widget.attrs["placeholder"] = _(
            "https://example.com"
        )
