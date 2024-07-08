from django.urls import path, include
from .views import StyleGuideView

from project.urls import urlpatterns


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "institutional/",
        include(
            ("org_nossas.nossas.apps.urls.institutional", "institutional"),
            namespace="institutional",
        ),
    ),
    path("styleguide/", StyleGuideView.as_view())
] + urlpatterns
