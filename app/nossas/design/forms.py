from django import forms
from django.conf import settings
from django.utils.text import slugify

from entangled.forms import EntangledModelFormMixin
from .models import UIProperties


EMPTY_CHOICES = [("", "----")]

SPACING = ["0", "1", "2", "3", "4", "5", "auto"]

PADDING_Y_SPACING_CHOICES = EMPTY_CHOICES + [("py-" + x, x) for x in SPACING]

PADDING_X_SPACING_CHOICES = EMPTY_CHOICES + [("px-" + x, x) for x in SPACING]


class UIPaddingFormMixin(EntangledModelFormMixin):
    padding_x = forms.ChoiceField(choices=PADDING_X_SPACING_CHOICES, required=False)

    padding_y = forms.ChoiceField(choices=PADDING_Y_SPACING_CHOICES, required=False)

    class Meta:
        entangled_fields = {"attributes": ["padding_x", "padding_y"]}

    # def save(self, commit=True):
    #     self.instance = super().save(commit=commit)

    #     if hasattr(self, "uiproperties_ptr"):
    #         import ipdb;ipdb.set_trace()
    #         self.instance.uiproperties_ptr.attributes.update({
    #             **self.cleaned_data
    #         })

    #         if commit:
    #             self.instance.uiproperties_ptr.save()

    #     return self.instance


if hasattr(settings, "DESIGN_THEME_COLORS"):
    CORES_TEMAS = EMPTY_CHOICES + [
        ("bg-" + slugify(args[0]), args[0]) for args in settings.DESIGN_THEME_COLORS
    ]
else:
    CORES_TEMAS = EMPTY_CHOICES + [
        ("bg-primary", "Primary"),
        ("bg-secondary", "Secondary"),
        ("bg-green", "Green"),
        ("bg-yellow", "Yellow"),
        ("bg-pink", "Pink"),
    ]


class UIBackgroundFormMixin(EntangledModelFormMixin):
    background = forms.ChoiceField(choices=CORES_TEMAS, required=False)

    class Meta:
        entangled_fields = {"attributes": ["background"]}


class UIBorderFormMixin(EntangledModelFormMixin):
    border_start = forms.BooleanField(required=False)
    border_end = forms.BooleanField(required=False)
    border_top = forms.BooleanField(required=False)
    border_bottom = forms.BooleanField(required=False)

    class Meta:
        entangled_fields = {
            "attributes": ["border_start", "border_end", "border_top", "border_bottom"]
        }
