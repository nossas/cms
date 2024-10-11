from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from .views import StyleGuideView


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "institutional/",
        include(
            ("org_nossas.nossas.apps.urls.institutional", "institutional"),
            namespace="institutional",
        ),
    ),
    path("styleguide/", StyleGuideView.as_view()),
    path("monitoring/", include("django_prometheus.urls")),
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("actions/", include("contrib.actions.pressure.urls")),
    path("", include("cms.urls")),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = "contrib.frontend.views.error_404"
handler500 = "contrib.frontend.views.error_500"

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)