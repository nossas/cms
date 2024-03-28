from django.urls import path

from .views import PublicationDetailView


urlpatterns = [
    path("<slug:slug>/", PublicationDetailView.as_view(), name="detail"),
]