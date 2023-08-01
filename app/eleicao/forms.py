from django import forms

from .models import Address, Candidate, PollingPlace


class Candidate1Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "email", "birth", "occupation", "slug"]


class Candidate2Form(forms.ModelForm):
    number = forms.IntegerField(label="Numero do candidato")
    # zone = forms.ModelChoiceField(PollingPlace.objects)

    class Meta:
        model = Address
        fields = [
            "state",
            "city",
            "neighborhood",
            # "zone",
            "number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["city"].widget = forms.Select()
        self.fields["neighborhood"].widget = forms.Select()


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

        self.fields["themes"].widget = forms.CheckboxSelectMultiple


class Candidate6Form(forms.Form):
    agree = forms.BooleanField(
        label="Li e estou de acordo com os compromissos listados assim"
    )
