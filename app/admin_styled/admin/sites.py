from typing import Any, Dict, Optional
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse


class AdminStyledSite(admin.AdminSite):
    site_header = "Administração"
    index_template = "admin_styled/custom/admin_index.html"

    def index(
        self, request: WSGIRequest, extra_context: Dict[str, Any] | None = ...
    ) -> TemplateResponse:
        title = f"Olá {request.user.first_name}, você está acessando o admin de {request.current_site.domain}"

        return super(AdminStyledSite, self).index(
            request, extra_context={"title": title}
        )

    # def each_context(self, request: Any) -> Any:
    #     context = super(AdminStyledSite, self).each_context(request)

    #     context.update({
    #         "index_title": f"{self.index_title}: {request.current_site.domain}"
    #     })

    #     return context
