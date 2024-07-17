from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import CandidateCreateView, CandidateDetailView, suggest_slug
from .places.views import fetch_cep

urlpatterns = [
    path("candidaturas/cadastro/", CandidateCreateView.as_view(), name="candidate_create"),
    # Filtro de endereço
    path("cep/", fetch_cep, name="cep"),
    # Sugere uma slug
    path("slug/", suggest_slug, name="slug"),
    # Precisa ser o último item da lista
    path("c/<slug:slug>/", CandidateDetailView.as_view(), name="candidate_detail"),
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