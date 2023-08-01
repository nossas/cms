from django.urls import path
from .views import CandidateView, CandidateCreateView, CandidateDetailView

urlpatterns = [
    path("candidatas/", CandidateView.as_view()), 
    path("candidatas/criar/", CandidateCreateView.as_view()),
    path("candidatas/<slug:slug>/", CandidateDetailView.as_view())
    ]

