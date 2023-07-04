from django.urls import path

from .views import pressure_submit_ajax


urlpatterns = [
    path("pressure/ajax/", pressure_submit_ajax, name="action_pressure"),
]