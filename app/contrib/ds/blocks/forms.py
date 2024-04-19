from django import forms

from colorfield.widgets import ColorWidget
from django_jsonform.forms.fields import JSONFormField
from entangled.forms import EntangledModelFormMixin

from .models import Block, ContainerSize, AlignmentItems, FlexWrap, FlexDirection


class ContainerFormMixin(EntangledModelFormMixin):
    size = forms.TypedChoiceField(
        choices=ContainerSize.choices, coerce=str, required=False
    )

    class Meta:
        entangled_fields = {"attributes": ["size"]}


class BackgroundFormMixin(EntangledModelFormMixin):
    background_color = forms.CharField(widget=ColorWidget(), required=False)

    class Meta:
        entangled_fields = {"attributes": ["background_color"]}


class SpacingFormMixin(EntangledModelFormMixin):
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
                    "spacing": {
                        "type": "string",
                        "choices": ["0", "1", "2", "3", "4", "5", "auto"],
                    },
                },
            },
        },
        required=False,
    )

    class Meta:
        entangled_fields = {"attributes": ["padding"]}


class GridFormMixin(EntangledModelFormMixin):
    gap = forms.IntegerField(
        initial=0, help_text="Unidade de medida em 'rem'", required=False
    )
    alignment = forms.ChoiceField(
        choices=[("", "----")] + AlignmentItems.choices, required=False
    )

    class Meta:
        entangled_fields = {"attributes": ["gap", "alignment"]}


class FlexFormMixin(EntangledModelFormMixin):
    direction = forms.ChoiceField(
        choices=[("", "----")] + FlexDirection.choices, required=False
    )
    wrap = forms.ChoiceField(choices=[("", "----")] + FlexWrap.choices, required=False)
    fill = forms.BooleanField(required=False)

    class Meta:
        entangled_fields = {"attributes": ["direction", "wrap", "fill"]}


class BlockForm(
    GridFormMixin,
    FlexFormMixin,
    BackgroundFormMixin,
    SpacingFormMixin,
    ContainerFormMixin,
    forms.ModelForm,
):

    class Meta:
        model = Block
        untangled_fields = ["element", "layout", "is_container"]
        entangled_fields = {"attributes": []}
