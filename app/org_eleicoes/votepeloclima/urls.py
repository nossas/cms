"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path

from .candidature.views import PublicCandidatureView
from .candidature.views.create import CreateUpdateCandidatureView
from .candidature.views.oauth import DashboardView, UpdateCandidatureStatusView
from .candidature.views.public import AddressView
from .candidature.filters.views import CandidatureSearchView

from .views import home

register_view = CreateUpdateCandidatureView.as_view(url_name="register_step", done_step_name="concluir")

urlpatterns = [
    # LoginRequired
    path("area-da-candidatura/", DashboardView.as_view(), name="dashboard"),
    # Public Routers
    re_path(r"^candidatura/cadastro/(?P<step>.+)/$", register_view, name="register_step",),
    path("candidatura/cadastro/", register_view, name="register"),
    path('candidatura/busca/', CandidatureSearchView.as_view(), name='candidature_search'),
    re_path(r"^c(andidatura)*/(?P<slug>.+)/$", PublicCandidatureView.as_view(), name='candidate_profile'),
    # API
    path('api/candidatura/buscar-endereco/', AddressView.as_view(), name='address'),
    path("api/candidatura/validar/", UpdateCandidatureStatusView.as_view()),
    # Manage
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("", home),
    path("", include("cms.urls")),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = "contrib.frontend.views.error_404"
handler500 = "contrib.frontend.views.error_500"

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
