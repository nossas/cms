from django.urls import path

from .views import CandidateCreateView, CandidateDetailView, suggest_slug
from .places.views import fetch_cep

urlpatterns = [
    path("candidaturas/cadastro/", CandidateCreateView.as_view(), name="candidate_create"),
    # Filtro de endereço
    path("cep/", fetch_cep, name="cep"),
    # Sugere uma slug
    path("slug/", suggest_slug, name="slug"),
    # Precisa ser o último item da lista
    path("c/<slug:slug>/", CandidateDetailView.as_view(), name="candidate_detail"),
]