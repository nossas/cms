from django import forms
from django_select2 import forms as s2forms


from ..models import Voter


class PlacesWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "places__state__icontains",
        "places__city__icontains",
        "places__neighborhood__icontains",
    ]


class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["name", "email", "whatsapp", "state", "city"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Seu nome completo"}),
            "email": forms.EmailInput(attrs={"placeholder": "Seu email"}),
            "whatsapp": forms.TextInput(
                attrs={
                    "placeholder": "Seu whatsapp",
                    "data-mask": "00 0 0000-0000",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["city"].widget = forms.Select()
