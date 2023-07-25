from django import forms

from ..models import Target


class TargetAdminForm(forms.ModelForm):
    class Meta:
        model = Target
        exclude = ["publish_on"]
