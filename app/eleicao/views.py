from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
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


class CandidateCreateView(CreateView):
    template_name = "eleicao/candidate_form.html"
    model = Candidate
    fields = "__all__"


class CandidateDetailView(DetailView):
    template_name = "eleicao/candidate_detail.html"
    model = Candidate
