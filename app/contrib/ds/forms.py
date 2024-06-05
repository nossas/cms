from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from .models import Menu

SPACING = [
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

class SpacingFormMixin(EntangledModelFormMixin):
    gap = forms.ChoiceField(choices=SPACING, required=False)
    gap_mobile = forms.ChoiceField(choices=SPACING, required=False)
    padding_top = forms.ChoiceField(choices=SPACING, required=False)
    padding_bottom = forms.ChoiceField(choices=SPACING, required=False)

    class Meta:
        untangled_fields = ["color"]
        entangled_fields = {
            "attributes": [
                "gap",
                "gap_mobile",
                "padding_top",
                "padding_bottom"
            ]
        }

class MenuForm(SpacingFormMixin, forms.ModelForm):
    class Meta:
        model = Menu
        fields = "__all__"
