from django import forms
from django_select2 import forms as s2forms

from ..models import Address, Candidate, Voter, PollingPlace


class Candidate1Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "email", "birth", "occupation", "slug"]
        widgets = {'birth': forms.TextInput(attrs={'data-mask':"00/00/0000"})}

class Candidate2Form(forms.ModelForm):
    number = forms.IntegerField(label="Numero do candidato")

    class Meta:
        model = Address
        fields = [
            "state",
            "city",
            "neighborhood",
            "number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["state"].widget = s2forms.Select2Widget()
        self.fields["city"].widget = forms.Select()
        self.fields["neighborhood"].widget = forms.Select()


class Candidate3Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["gender", "is_trans", "race", "is_reelection"]


class Candidate4Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["bio", "photo", "video", "social_media", "social_media_2"]


class Candidate6Form(forms.Form):
    agree = forms.BooleanField(
        label="Li e estou de acordo com os compromissos listados assim"
    )


class PlacesWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "places__state__icontains",
        "places__city__icontains",
        "places__neighborhood__icontains",
    ]


class VoterForm(forms.ModelForm):
    zone = forms.ModelChoiceField(
        queryset=PollingPlace.objects.all(), label="Onde você vota?", required=True
    )

    class Meta:
        model = Voter
        fields = ["name", "email", "whatsapp", "zone"]
