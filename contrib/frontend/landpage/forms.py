from django import forms
from django.db import models


class LayoutChoices(models.TextChoices):
    empty = "", "---"
    hero = "hero", "Hero"
    hero_nobrand = "hero_nobrand", "Hero Sem logo"
    tree_columns = "tree_columns", "3 Colunas"
    four_columns = "four_columns", "4 Colunas"
    two_columns_a = "two_columns_a", "2 Colunas - 6x6"
    two_columns_b = "two_columns_b", "2 Colunas - 4x8"
    signature = "signature", "Assinatura"
    signature_partners_a = (
        "signature_partners_a",
        "2 Colunas - Assinatura com parceiros",
    )
    signature_partners_b = "signature_partners_b", "1 Coluna - Assinatura com parceiros"
    pressure = "pressure", "Pressão"


class LayoutBlockForm(forms.ModelForm):
    layout = forms.CharField(
        label="Layout",
        required=False,
        widget=forms.Select(
            choices=LayoutChoices.choices
        )
    )