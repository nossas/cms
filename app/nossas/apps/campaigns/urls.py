from django.urls import path

from .views import CampaignDetailView


urlpatterns = [
    path("<int:pk>/", CampaignDetailView.as_view(), name="campaign-detail"),
]