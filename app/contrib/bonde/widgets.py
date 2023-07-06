from typing import Any
from django_select2 import forms as s2forms
from .models import Widget


class ActionSelectWidget(s2forms.Select2Widget):
    """
    """
    empty_label = "Busque pelo nome ou pelo id da widget"


class ActionChoices:
    """
    """

    def __init__(self, kind: str):
        self.kind = kind
    

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        qs = Widget.objects.on_site().filter(kind=self.kind)

        return list(
            map(lambda x: (x.id, f"{x.block.mobilization.name} ({x.id})"), qs.all())
        )