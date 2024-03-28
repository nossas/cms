from django.urls import path

from ..views.timeline import TimelineDetailView

urlpatterns = [
    path('event/<int:pk>/', TimelineDetailView.as_view(), name='event_detail'),
]
