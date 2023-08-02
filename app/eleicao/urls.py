from django.urls import path
from .views import CandidateListView, CandidateCreateView, CandidateDetailView, VoterCreateView, ResultsCandidateView
from .places.views import fetch_cep

urlpatterns = [
    path("candidaturas/", CandidateListView.as_view(), name="candidate_list"),
    path("candidaturas/cadastro/", CandidateCreateView.as_view(), name="candidate_create"),
    # Filtro de endereço
    path("cep/", fetch_cep, name="cep"),
    path("querovotar/", VoterCreateView.as_view(), name="voter_match"),
    path("querovotar/resultado/", ResultsCandidateView.as_view(), name="voter_match_result"),
    path("<slug:slug>/", CandidateDetailView.as_view(), name="candidate_detail"),
  
]
