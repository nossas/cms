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

from .candidature.views import RegisterView, EditRegisterView, DashboardView

register_view = RegisterView.as_view(url_name="register_step", done_step_name="concluir")
register_edit_view = EditRegisterView.as_view(url_name="register_edit_step", done_step_name="concluir")

urlpatterns = [
    # path("monitoring/", include("django_prometheus.urls")),
    re_path(
        r"^register/edit/(?P<step>.+)/$",
        register_edit_view,
        name="register_edit_step",
    ),
    path("register/edit/", register_edit_view, name="register_edit"),
    re_path(
        r"^register/(?P<step>.+)/$",
        register_view,
        name="register_step",
    ),
    path("register/", register_view, name="register"),
    path("oauth/", DashboardView.as_view()),
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
