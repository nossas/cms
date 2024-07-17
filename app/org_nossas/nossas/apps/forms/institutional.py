from django import forms


class InstitutionalInformationForm(forms.ModelForm):

    class Meta:
        widgets = {
            "zipcode":  forms.TextInput(
                attrs={
                    "data-mask": "00.000-000",
                }
            ),
            "contact_phone": forms.TextInput(
                attrs={
                    "data-mask": "(00) 0 0000-0000",
                }
            ),
        }