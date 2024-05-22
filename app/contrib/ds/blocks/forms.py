from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.widgets import ColorWidget
from django_jsonform.forms.fields import JSONFormField
from entangled.forms import EntangledModelFormMixin
from filer.fields.image import FilerImageField

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


SPACINGS = [
    ("0", "0", ),
    ("1", "1", ),
    ("2", "2", ),
    ("3", "3", ),
    ("4", "4", ),
    ("5", "5", ),
    ("6", "6", ),
    ("7", "7", ),
    ("8", "8", ),
    ("auto", "auto", ),
]


class SpacingFormMixin(EntangledModelFormMixin):
    padding_top = forms.ChoiceField(choices=SPACINGS)
    padding_bottom = forms.ChoiceField(choices=SPACINGS)
    padding_right = forms.ChoiceField(choices=SPACINGS)
    padding_left = forms.ChoiceField(choices=SPACINGS)

    class Meta:
        entangled_fields = {
            "attributes": [
                "padding_top",
                "padding_bottom",
                "padding_right",
                "padding_left",
            ]
        }


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
    alignment_mobile = forms.ChoiceField(
        choices=[("", "----")] + AlignmentItems.choices,
        required=False,
        label=_("Alinhamento (Mobile)"),
        help_text=_("Como os elementos são alinhados"),
        widget=forms.RadioSelect(attrs={"class": "hidden"}),
    )

    class Meta:
        entangled_fields = {"attributes": ["gap", "alignment", "alignment_mobile"]}


class FlexFormMixin(EntangledModelFormMixin):
    direction = forms.ChoiceField(
        choices=[("", "----")] + FlexDirection.choices,
        required=False,
        label=_("Direção"),
        help_text=_("Escolha como os elementos se alinharão"),
    )
    direction_mobile = forms.ChoiceField(
        choices=[("", "----")] + FlexDirection.choices,
        required=False,
        label=_("Direção (Mobile)"),
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
        entangled_fields = {"attributes": ["direction", "direction_mobile", "wrap", "fill"]}


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
        untangled_fields = ["template", "element", "layout", "is_container", "background_image", "background_size"]
        entangled_fields = {"attributes": []}


class BlockTemplate(models.TextChoices):
    empty = "", "Vazio"
    content_call_to_action = "content_call_to_action", "CTA"
    content_one_col = "content_one_col", "1 coluna"
    content_three_cols = "content_three_cols", "3 colunas"
    content_two_cols_6x6 = "content_two_cols_6x6", "2 colunas (6x6)"
    content_two_cols_4x8 = "content_two_cols_4x8", "2 colunas (4x8)"
    content_four_cols = "content_four_cols", "4 colunas"


class BlockTemplateForm(BlockForm):
    template = forms.ChoiceField(
        choices=BlockTemplate.choices, initial=BlockTemplate.empty, required=False,
        help_text=_("Selecione um tipo de bloco para adicionar à página")
    )

    class Meta:
        model = Block
        untangled_fields = ["template", "element", "layout", "is_container", "background_image", "background_size"]
        entangled_fields = {"attributes": []}
        help_texts = {
            'background_image': 'Selecione uma imagem para o background do bloco.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["element"].initial = BlockElement.section
        self.fields["is_container"].initial = True
        self.fields["padding_top"].initial = '4'
        self.fields["padding_bottom"].initial = '4'
