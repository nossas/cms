from django.urls import path

from .views import submit_form_json


urlpatterns = [
    path('submit/', submit_form_json, name='bondewidgets_forms_submit'),
]