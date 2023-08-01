from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Candidate

# Create your views here.


class CandidateView(ListView):
    template_name = "eleicao/candidate_list.html"
    model = Candidate


class CandidateCreateView(CreateView):
    template_name = "eleicao/candidate_form.html"
    model = Candidate
    fields = "__all__"
    

class CandidateDetailView(DetailView):
    template_name = "eleicao/candidate_detail.html"
    model = Candidate
