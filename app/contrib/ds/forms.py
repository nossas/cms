from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from .models import Menu

GAP_CHOICES = [
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("auto", "auto"),
]

class GapFormMixin(EntangledModelFormMixin):
    gap = forms.ChoiceField(choices=GAP_CHOICES, required=False)
    gap_mobile = forms.ChoiceField(choices=GAP_CHOICES, required=False)

    class Meta:
        untangled_fields = ["color"]
        entangled_fields = {
            "attributes": [
                "gap",
                "gap_mobile",
            ]
        }

class MenuForm(GapFormMixin, forms.ModelForm):
    class Meta:
        model = Menu
        fields = "__all__"
