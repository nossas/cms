from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.widgets import ColorWidget
from django_jsonform.forms.fields import JSONFormField
from entangled.forms import EntangledModelFormMixin

from .models import (
    Block,
    ContainerSize,
    AlignmentItems,
    FlexWrap,
    FlexDirection,
    BlockElement,
)


class ContainerFormMixin(EntangledModelFormMixin):
    size = forms.TypedChoiceField(
        choices=ContainerSize.choices, coerce=str, required=False
    )

    class Meta:
        entangled_fields = {"attributes": ["size"]}


class BackgroundFormMixin(EntangledModelFormMixin):
    background_color = forms.CharField(
        widget=ColorWidget(),
        required=False,
        label=_("Cor de fundo"),
        help_text=_("Selecione o background do bloco"),
    )

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
        initial=0,
        label=_("Gap (Distância entre items)"),
        help_text=_("Espaço entre conteúdos dentro do bloco"),
        required=False,
    )
    alignment = forms.ChoiceField(
        choices=[("", "----")] + AlignmentItems.choices,
        required=False,
        label=_("Alinhamento"),
        help_text=_("Como os elementos são alinhados"),
        widget=forms.RadioSelect(attrs={"class": "hidden"}),
    )

    class Meta:
        entangled_fields = {"attributes": ["gap", "alignment"]}


class FlexFormMixin(EntangledModelFormMixin):
    direction = forms.ChoiceField(
        choices=[("", "----")] + FlexDirection.choices,
        required=False,
        label=_("Direção"),
        help_text=_("Escolha como os elementos se alinharão"),
    )
    wrap = forms.ChoiceField(
        choices=[("", "----")] + FlexWrap.choices,
        required=False,
        label=_("Quebra de Linha"),
        help_text=_("Ajuste da quebra em uma ou várias linhas"),
    )
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
    template = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Block
        untangled_fields = ["template", "element", "layout", "is_container"]
        entangled_fields = {"attributes": []}


class BlockTemplate(models.TextChoices):
    empty = "", "empty"
    content_one_col = "content_one_col", "Conteúdo 1 coluna"
    content_three_cols = "content_three_cols", "Conteúdo 3 colunas"
    content_two_cols_6x6 = "content_two_cols_6x6", "Conteúdo 2 colunas (6x6)"
    content_two_cols_4x8 = "content_two_cols_4x8", "Conteúdo 2 colunas (4x8)"
    content_four_cols = "content_four_cols", "Conteúdo 4 colunas"


class BlockTemplateForm(BlockForm):
    template = forms.ChoiceField(
        choices=BlockTemplate.choices, initial=BlockTemplate.empty, required=False
    )

    class Meta:
        model = Block
        untangled_fields = ["template", "element", "layout", "is_container"]
        entangled_fields = {"attributes": []}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["element"].initial = BlockElement.section
        self.fields["is_container"].initial = True
        self.fields["padding"].initial = [{"side": "y", "spacing": "4"}]
