from django.urls import path, include

from project.urls import urlpatterns


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
] + urlpatterns