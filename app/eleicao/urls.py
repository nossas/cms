from django.urls import path
from .views import CandidateListView, CandidateCreateView, CandidateDetailView, VoterCreateView, ResultsCandidateView, suggest_slug
from .places.views import fetch_cep

urlpatterns = [
    path("candidaturas/", CandidateListView.as_view(), name="candidate_list"),
    path("candidaturas/cadastro/", CandidateCreateView.as_view(), name="candidate_create"),
    path("querovotar/", VoterCreateView.as_view(), name="voter_match"),
    path("querovotar/resultado/", ResultsCandidateView.as_view(), name="voter_match_result"),
    # Filtro de endereço
    path("cep/", fetch_cep, name="cep"),
    # Sugere uma slug
    path("slug/", suggest_slug, name="slug"),
    # Precisa ser o último item da lista
    path("<slug:slug>/", CandidateDetailView.as_view(), name="candidate_detail"),
]
