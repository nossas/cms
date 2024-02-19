from django.urls import path, include
from .views import StyleGuideView

from project.urls import urlpatterns


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "institutional/",
        include(
            ("nossas.apps.urls.institutional", "institutional"),
            namespace="institutional",
        ),
    ),
    path("styleguide/", StyleGuideView.as_view()),
    path("", include("djangocms_forms.urls")),
] + urlpatterns
