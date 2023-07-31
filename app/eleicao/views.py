from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Candidate

# Create your views here.


class CandidateView(ListView):
    template_name = "eleicao/candidate.html"
    model = Candidate

class CandidateCreateView(CreateView):
    template_name = "eleicao/candidate_form.html"
    model = Candidate
    fields = "__all__"