from typing import Any, List
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.cache import never_cache


class Opts:
    app_label = "cms"
    model_name = "page"


class AppSite(admin.AdminSite):
    site_header = "Admin2"
    index_template = "admin2/index.html"
    app_index_template = "admin2/app_index.html"
    login_template = "admin2/login.html"
    logout_template = "admin2/logout.html"
    # Novos atributos
    include_apps = ["pressure", "sites", "actions", "cms"]

    def get_app_list(self, request: WSGIRequest) -> List[Any]:
        app_list = super().get_app_list(request)
        return list(filter(lambda x: x["app_label"] in self.include_apps, app_list))

    @never_cache
    def index(self, request: WSGIRequest, extra_context=None):
        # Carregar informações no index do dashboard (admin)
        from django.contrib.sites.models import Site
        from cms.models.pagemodel import Page

        site = Site.objects.get_current(request)
        page_qs = (
            Page.objects.filter(node__site=site, publisher_is_draft=True)
            .select_related("node")
            .exclude(is_page_type=True)
        )

        extra_context = {
            "admin2": {
                "pages": page_qs,
                "page_opts": Opts(),
            }
        }

        return super().index(request, extra_context)
