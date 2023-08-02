from django import forms
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.functional import lazy

# from django_select2 import forms as s2forms

from ..csv.choices import get_states


class CandidateListFilter(forms.Form):
    uf = forms.ChoiceField(
        label="Estado",
        choices=lazy(get_states, list)(),
        widget=forms.Select(
            attrs={"class": "w-full max-w-xs select select-bordered rounded-lg bg-[#EFEFEF] border-[#E0E0E0]"}
        )
    )

    def as_html(self):
        template_name = "eleicao/filters/candidate_list_filter.html"

        _html = render(None, template_name, { "form": self }).content.decode("utf-8")

        return mark_safe(_html)
