from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("", include("cms.urls")),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = "contrib.frontend.views.error_404"
handler500 = "contrib.frontend.views.error_500"

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)