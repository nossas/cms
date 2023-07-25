from typing import Any

from django_select2 import forms as s2forms

from .models import Campaign


class CampaignChoices:
    """ """

    # def __init__(self, kind: str):
    #     self.kind = kind

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        qs = Campaign.objects.all()

        return list(
            map(lambda x: (x.id, f"{x.name} -({x.slug})"), qs.all())
        )


class CampaignSelectWidget(s2forms.Select2Widget):
    """ """

    empty_label = "Busque pelo nome ou pelo slug da Campanha"