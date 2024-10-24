from django import forms
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

from org_nossas.nossas.design.widgets import CharsLeftTextInput, CharsLeftTextarea

from ..models.timeline import TimelineEvent

def get_events_year_choices():
    years = TimelineEvent.on_site.order_by('-year').values_list('year', flat=True).distinct()
    return [((year), year) for year in years]

class TimelineFilterForm(forms.Form):
    year = forms.ChoiceField(
        label=_("Ano"),
        choices=lazy(get_events_year_choices, list)(),
        widget=forms.Select(attrs={
            "class": "selectpicker",
            "title": "Selecione um ano",
            "data-width": "fit",
            "data-allow-clear": "true"
            }),
        required=False,
    )



class TimelineEventForm(forms.ModelForm):

    class Meta:
        model = TimelineEvent
        fields = "__all__"
        widgets = {
            "description": CharsLeftTextarea(attrs={"maxlength": 200})
        }