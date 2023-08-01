from django import forms

from .models import Candidate


class Candidate1Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "email", "slug"]


class Candidate2Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["state", "city", "neighborhood", "zone", "number"]


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


class Candidate6Form(forms.Form):
    agree = forms.BooleanField(
        label="Li e estou de acordo com os compromissos listados assim"
    )
