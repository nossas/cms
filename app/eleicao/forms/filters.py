from django import forms
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.functional import lazy

from django.urls import reverse_lazy

# from django_select2 import forms as s2forms

from ..csv.choices import get_states


class CandidateListFilter(forms.Form):
    uf = forms.ChoiceField(
        label="Estado",
        choices=lazy(get_states, list)(),
        widget=forms.Select(
            attrs={
                "data-cep-fields": "state",
                "data-cep-url": reverse_lazy("eleicao:cep"),
            }
        )
    )

    city = forms.CharField(
        label="Cidade",
        widget=forms.Select(
            attrs={
                "data-cep-fields": "city",
                "data-cep-url": reverse_lazy("eleicao:cep"),
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['uf'].widget.choices = [('', 'Todos'), ] + self.fields['uf'].widget.choices

    def as_html(self):
        template_name = "eleicao/filters/candidate_list_filter.html"

        _html = render(None, template_name, { "form": self }).content.decode("utf-8")

        return mark_safe(_html)
