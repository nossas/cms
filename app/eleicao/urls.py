from django.urls import path
from .views import CandidateView, CandidateCreateView, CandidateDetailView, VoterCreateView
from .places.views import fetch_cep

urlpatterns = [
    path("candidatas/", CandidateView.as_view(), name="candidate_list"),
    path("candidatas/criar/", CandidateCreateView.as_view(), name="candidate_create"),
    path("candidatas/<slug:slug>/", CandidateDetailView.as_view(), name="candidate_detail"),
    # Filtro de endereço
    path("cep/", fetch_cep, name="cep"),
    path("querovotar/descubra/", VoterCreateView.as_view(), name="voter_match"),
]
