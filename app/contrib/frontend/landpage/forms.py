from django import forms
from django.db import models

from .models import Block
from .widgets import SelectLayout


class LayoutChoices(models.TextChoices):
    # empty = "empty", "---"
    hero = "hero", "Capa 1 coluna"
    hero_nobrand = "hero_nobrand", "Conteúdo 1 coluna"
    tree_columns = "tree_columns", "Conteúdo 3 colunas"
    two_columns_a = "two_columns_a", "Conteúdo 2 colunas (6x6)"
    two_columns_b = "two_columns_b", "Conteúdo 2 colunas (4x8)"
    four_columns = "four_columns", "Conteúdo 4 colunas"
    five_columns = "five_columns", "Conteúdo 5 colunas"
    signature = "signature", "Assinatura 2 colunas"
    signature_partners_a = (
        "signature_partners_a",
        "Assinatura + parceiros 2 colunas",
    )
    signature_partners_b = "signature_partners_b", "Parceiros 1 coluna"
    pressure = "pressure", "Pressão"


class LayoutBlockForm(forms.ModelForm):
    layout = forms.CharField(
        label="Layout",
        required=False,
        widget=SelectLayout(
            choices=LayoutChoices.choices
        )
    )

    class Meta:
        model = Block
        fields = "__all__"



class LayoutBlockPressureForm(forms.ModelForm):
    layout = forms.CharField(
        label="Layout",
        required=False,
        widget=SelectLayout(
            choices=LayoutChoices.choices
        )
    )

    class Meta:
        model = Block
        fields = "__all__"