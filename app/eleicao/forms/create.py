from django import forms
from django_select2 import forms as s2forms

from ..models import Address, Candidate, Voter, PollingPlace


class Candidate1Form(forms.Form):
    agree = forms.BooleanField(
        label="Li e estou de acordo com os compromissos listados assim"
    )

class Candidate2Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "email", "birth", "slug"]


class Candidate3Form(forms.ModelForm):
    class Meta:
        model = Candidate
        widgets = {
            "is_trans": forms.RadioSelect,
            "is_reelection": forms.RadioSelect
        }
        fields = [
            "occupation",
            "gender",
            "is_trans",
            "race",
            "is_reelection"
        ]

class Candidate4Form(forms.ModelForm):
    number = forms.IntegerField(label="Numero do candidato")
    # zone_id = forms.IntegerField()

    class Meta:
        model = Address
        fields = [
            "state",
            "city",
            "neighborhood",
            # "zone_id",
            "number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["state"].widget = s2forms.Select2Widget()
        self.fields["city"].widget = forms.Select()
        self.fields["neighborhood"].widget = forms.Select()
        # self.fields["zone_id"].widget = forms.Select()

class Candidate5Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["bio", "photo", "video", "social_media"]


class Candidate6Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["themes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["themes"].widget = forms.CheckboxSelectMultiple(
            choices=list(map(lambda x: x, Theme.objects.values_list("id", "label")))
        )

class PlacesWidget(s2forms.ModelSelect2Widget):
  
  search_fields = [
    "places__state__icontains", 
    "places__city__icontains",
    "places__neighborhood__icontains"
  ]
class VoterForm(forms.ModelForm):
  


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
