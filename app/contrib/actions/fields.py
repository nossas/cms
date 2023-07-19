from typing import Any
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model
from django_select2.forms import Select2Widget

from .models import Campaign


def get_choices():
    qs = Campaign.objects

    return list(map(lambda x: (x.id, f"{x.name} ({x.slug})"), qs.all()))


def parse_campaign(id: int) -> Any:
    obj = Campaign.objects.get(id=id)
    if not obj:
        raise ValidationError(f"Campaign {id} not found")

    return obj


class CampaignField(models.IntegerField):
    description = "A campaign of Bonde (bridge style)"

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = get_choices()

        super().__init__(*args, **kwargs)

    def from_db_value(
        self, value: int | None, expression, connection
    ) -> Campaign | None:
        if value is None:
            return value

        return parse_campaign(value)

    def to_python(self, value: int | Campaign | None) -> Campaign | None:
        if isinstance(value, Campaign):
            return value

        if value is None:
            return value

        return parse_campaign(value)

    def get_prep_value(self, value: Campaign) -> int:
        return value.id

    def formfield(self, **kwargs):
        defaults = {"widget": Select2Widget}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def value_from_object(self, obj):
        # Used on django forms to render value
        value = super().value_from_object(obj)
        return value.id

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ("choices",)

    def validate(self, value: Campaign, model_instance: Model) -> None:
        return super().validate(value.id, model_instance)
