from typing import Any, Dict
from collections import ChainMap

from django.db import models, transaction
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.core.files.storage import DefaultStorage
from django.utils.text import slugify
from django.http import JsonResponse


from formtools.wizard.views import SessionWizardView

from .bonde_utils import create_form_entry
from .forms import (
    Candidate1Form,
    Candidate2Form,
    Candidate3Form,
    Candidate4Form,
    Candidate5Form,
    Candidate6Form,
    Candidate7Form,
    VoterForm
)
from .forms.filters import CandidateListFilter
from .models import Candidate, Voter, PollingPlace, CandidateStatusChoices

# Create your views here.


class CandidateListView(ListView):
    template_name = "eleicao/candidate_list.html"
    model = Candidate
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = CandidateListFilter(self.request.GET)

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(status=CandidateStatusChoices.published)

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
        Candidate7Form
    ]

    file_storage = DefaultStorage()

    # model = Candidate
    # fields = "__all__"

    def process_step_files(self, form):
        return self.get_form_step_files(form)

    @transaction.atomic
    def done(self, form_list, **kwargs):
        values = list(map(lambda form: form.cleaned_data, form_list))
        values = dict(ChainMap(*values))
        # import ipdb; ipdb.set_trace()
        # Processar os valores
        values.pop("agree")
        values.pop("agree_2")
        values.pop("agree_3")
        values.pop("agree_4")
        values.pop("agree_5")
        values.pop("agree_6")
        values.pop("agree_7")
        values.pop("agree_8")
        values.pop("agree_9")
        values.pop("agree_10")
        values.pop("agree_11")
        values.pop("agree_12")
        
        # PollingPlace
        state = values.pop("state")
        city = values.pop("city")
        place_id = values.pop("place")

        values["place_id"] = int(place_id)

        photo = values.pop("photo")
        video = values.pop("video")
        obj = Candidate.objects.create(**values, photo=photo, video=video)
        obj.save()

        # Integrate with Bonde

        fe = create_form_entry(state=state, city=city, **values)

        print(fe)

        return redirect(obj.get_absolute_url() + '?modal=true')


class CandidateDetailView(DetailView):
    template_name = "eleicao/candidate_detail.html"
    model = Candidate

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        modal = self.request.GET.get('modal')

        if modal:
            ctx.update({
                "modal_is_open": True
            })

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(status=CandidateStatusChoices.published)


class VoterCreateView(CreateView):
    template_name = "eleicao/voter_form.html"
    form_class = VoterForm
    model = Voter


class ResultsCandidateView(ListView):
    template_name = "eleicao/voter_results.html"
    model = Candidate

    def get_queryset(self) -> QuerySet[Any]:
        qs = Candidate.objects.filter(status=CandidateStatusChoices.published)

        filter_state = self.request.GET.get("uf", None)
        filter_zone = self.request.GET.get("zone", None)
        if filter_state:
            return qs.filter(state__iexact=filter_state)
        if filter_zone:
            return qs.filter(zone=filter_zone)

        return qs


# Sugerir uma slug
def suggest_slug(request):
    name = request.GET.get("name")
    slug = slugify(name).replace("-", "")
    suggestion = slug
    list_candidate = Candidate.objects.filter(status=CandidateStatusChoices.published).filter(slug=slug)
    total = list_candidate.count()
    sufix = 1
    while total > 0:
        suggestion = slug + f"{sufix}"
        list_candidate = Candidate.objects.filter(status=CandidateStatusChoices.published).filter(slug=suggestion)
        total = list_candidate.count()
        sufix = sufix + 1

    return JsonResponse({"slug": suggestion})
