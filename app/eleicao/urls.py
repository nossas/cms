from django.urls import path
from .views import CandidateView, CandidateCreateView, CandidateDetailView, VoterCreateView
from .places.views import fetch_cep

urlpatterns = [
    path("candidatas/", CandidateView.as_view()),
    path("candidatas/criar/", CandidateCreateView.as_view()),
    path("candidatas/<slug:slug>/", CandidateDetailView.as_view()),
    # Filtro de endereço
    path("cep/", fetch_cep),
    path("querovotar/descubra/", VoterCreateView.as_view()),
]
