from django import forms
from django_select2.forms import ModelSelect2MultipleWidget

from ..models.base import Pressure, EmailPressure, PhonePressure, TwitterPressure
# from ..models.plugins import PressurePluginModel



class EmailPressureForm(forms.ModelForm):
    class Meta:
        model = EmailPressure
        # fields = "__all__"
        exclude = ["plugin"]


class PhonePressureForm(forms.ModelForm):
    class Meta:
        model = PhonePressure
        # fields = "__all__"
        exclude = ["plugin"]


class TwitterPressureForm(forms.ModelForm):
    class Meta:
        model = TwitterPressure
        # fields = "__all__"
        exclude = ["plugin"]


class MultipleTargetSelect(ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class PressureAdminForm(forms.ModelForm):
    class Meta:
        model = Pressure
        widgets = {"targets": MultipleTargetSelect}
        fields = "__all__"


class PressureAdminChangeForm(PressureAdminForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields["campaign"].disabled = True
