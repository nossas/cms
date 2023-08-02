from django import forms
from django_select2 import forms as s2forms

from .models import Address, Candidate, Theme


class Candidate1Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "email", "birth", "occupation", "slug"]


class Candidate2Form(forms.ModelForm):
    number = forms.IntegerField(label="Numero do candidato")
    zone_id = forms.IntegerField()

    class Meta:
        model = Address
        fields = [
            "state",
            "city",
            "neighborhood",
            "zone_id",
            "number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["state"].widget = s2forms.Select2Widget()
        self.fields["city"].widget = forms.Select()
        self.fields["neighborhood"].widget = forms.Select()
        self.fields["zone_id"].widget = forms.Select()


class Candidate3Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["gender", "is_trans", "race", "is_reelection"]


class Candidate4Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["bio", "photo", "video", "social_media"]


class Candidate5Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["themes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["themes"].widget = forms.CheckboxSelectMultiple(
            choices=list(map(lambda x: x, Theme.objects.values_list("id", "label")))
        )


class Candidate6Form(forms.Form):
    agree = forms.BooleanField(
        label="Li e estou de acordo com os compromissos listados assim"
    )
