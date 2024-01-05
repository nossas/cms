from django import forms
from django.conf import settings
from django.utils.text import slugify

from django_jsonform.forms.fields import JSONFormField
from entangled.forms import EntangledModelFormMixin
from djangocms_frontend.fields import ButtonGroup
from .models import UIProperties


EMPTY_CHOICES = [("", "----")]

SPACING = ["0", "1", "2", "3", "4", "5", "auto"]


class UIPaddingFormMixin(EntangledModelFormMixin):
    padding = JSONFormField(
        schema={
            "type": "array",
            "items": {
                "type": "dict",
                "keys": {
                    "side": {
                        "type": "string",
                        "choices": [
                            {"title": "*-top", "value": "t"},
                            {"title": "*-right", "value": "r"},
                            {"title": "*-bottom", "value": "b"},
                            {"title": "*-left", "value": "l"},
                            {"title": "*-left & *-right", "value": "x"},
                            {"title": "*-top & *-bottom", "value": "y"},
                        ],
                    },
                    "spacing": {"type": "string", "choices": SPACING},
                },
            },
        },
        required=False
    )

    class Meta:
        entangled_fields = {"attributes": ["padding"]}


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


class BackgroundSelect(forms.RadioSelect):
    template_name = "design/fields/background_select.html"
    option_template_name = "design/fields/background_select_option.html"

    class Media:
        css = {"all": ("djangocms_frontend/css/button_group.css",)}


class UIBackgroundFormMixin(EntangledModelFormMixin):
    background = forms.ChoiceField(
        choices=CORES_TEMAS, required=False, widget=BackgroundSelect()
    )

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
