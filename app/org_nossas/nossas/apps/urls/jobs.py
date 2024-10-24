from django.urls import path

from ..views.jobs import JobDetailView


urlpatterns = [
    path("<int:pk>/", JobDetailView.as_view(), name="job-detail"),
]