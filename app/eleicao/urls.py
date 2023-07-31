from django.urls import path
from .views import CandidateView, CandidateCreateView

urlpatterns = [
    path("candidatas/", CandidateView.as_view()), 
    path("candidatas/criar", CandidateCreateView.as_view())
    ]

