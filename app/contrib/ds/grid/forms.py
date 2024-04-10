from django import forms

from .models import Grid

COLUMNS_CHOICES = (
    (1, "1 coluna"),
    (2, "2 colunas"),
    (3, "3 colunas"),
    (4, "4 colunas"),
    (6, "6 colunas"),
)


class GridForm(forms.ModelForm):
    columns = forms.TypedChoiceField(
        required=False, choices=COLUMNS_CHOICES, coerce=int
    )

    class Meta:
        model = Grid
        fields = "__all__"
