from django.urls import path
from .views import CandidateListView, CandidateCreateView, CandidateDetailView, VoterCreateView
from .places.views import fetch_cep

urlpatterns = [
    path("candidaturas/", CandidateListView.as_view(), name="candidate_list"),
    path("candidaturas/cadastro/", CandidateCreateView.as_view(), name="candidate_create"),
    path("<slug:slug>/", CandidateDetailView.as_view(), name="candidate_detail"),
    # Filtro de endereço
    path("cep/", fetch_cep, name="cep"),
    path("querovotar/", VoterCreateView.as_view(), name="voter_match"),
]
