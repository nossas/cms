from django.urls import path

from .views import PressureFormAjaxView


urlpatterns = [
    path("pressure/ajax/", PressureFormAjaxView.as_view(), name="action_pressure"),
]