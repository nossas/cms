from django.urls import path

from ..views.institutional import redirect_add_or_change


urlpatterns = [
    path("redirect-add-or-change/", redirect_add_or_change, name="redirect_add_or_change"),
]