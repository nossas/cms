from typing import Any
from collections import ChainMap
from django.conf import settings
from django.db import transaction
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView
from formtools.wizard.views import SessionWizardView

from .forms import (
    Candidate1Form,
    Candidate2Form,
    Candidate3Form,
    Candidate4Form,
    Candidate5Form,
    Candidate6Form,
)
from .models import Candidate

# Create your views here.


class CandidateView(ListView):
    template_name = "eleicao/candidate_list.html"
    model = Candidate

    def get_queryset(self) -> QuerySet[Any]:
        filter_state = self.request.GET.get("uf", None)
        if filter_state:
            return Candidate.objects.filter(state__iexact=filter_state)

        return super().get_queryset()


class CandidateCreateView(SessionWizardView):
    template_name = "eleicao/candidate_wizard_form.html"
    form_list = [
        Candidate1Form,
        Candidate2Form,
        Candidate3Form,
        Candidate4Form,
        Candidate5Form,
        Candidate6Form,
    ]
    file_storage = settings.DEFAULT_FILE_STORAGE
    # model = Candidate
    # fields = "__all__"

    def process_step_files(self, form):
        return self.get_form_step_files(form)

    @transaction.atomic
    def done(self, form_list, **kwargs):
        values = list(map(lambda form: form.cleaned_data, form_list))
        values = dict(ChainMap(*values))

        # Processar os valores
        themes = values.pop("themes")
        values.pop("agree")

        obj = Candidate.objects.create(**values)
        obj.themes.set(themes)
        obj.save()

        return redirect(obj.get_absolute_url())


class CandidateDetailView(DetailView):
    template_name = "eleicao/candidate_detail.html"
    model = Candidate
