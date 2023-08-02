from typing import Any, Dict
from collections import ChainMap

from django.conf import settings
from django.db import transaction
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from formtools.wizard.views import SessionWizardView

from .forms import (
    Candidate1Form,
    Candidate2Form,
    Candidate3Form,
    Candidate4Form,
    Candidate5Form,
    Candidate6Form,
)
from .forms.filters import CandidateListFilter
from .models import Address, Candidate, Voter

# Create your views here.


class CandidateListView(ListView):
    template_name = "eleicao/candidate_list.html"
    model = Candidate
    paginate_by = 2

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = CandidateListFilter(self.request.GET)

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        
        filter_state = self.request.GET.get("uf", None)
        if filter_state:
            return qs.filter(place__state__iexact=filter_state)

        return qs


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
        values.pop("agree")
        # Theme
        themes = values.pop("themes")
        # Address
        state = values.pop("state")
        city = values.pop("city")
        neighborhood = values.pop("neighborhood")
        
        values["place_id"] = Address.objects.filter(
            state=state, city=city, neighborhood=neighborhood
        ).first().id
        # PollingPlace
        # zone = values.pop("zone")
        # polling_place = PollingPlace.objects.get(id=zone)

        obj = Candidate.objects.create(**values)
        # obj.zone = polling_place
        obj.themes.set(themes)
        obj.save()

        return redirect(obj.get_absolute_url())


class CandidateDetailView(DetailView):
    template_name = "eleicao/candidate_detail.html"
    model = Candidate


class VoterCreateView(CreateView):
    template_name = "eleicao/voter_form.html"
    model = Voter
    fields = "__all__"
