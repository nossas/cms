from typing import Any, List
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest


class AppSite(admin.AdminSite):

    site_header = "Admin2"
    index_template = "admin2/index.html"
    app_index_template = "admin2/app_index.html"
    login_template = "admin2/login.html"
    logout_template = "admin2/logout.html"
    # Novos atributos
    include_apps = ['pressure', 'sites', 'actions','cms']


    
    def get_app_list(self, request: WSGIRequest) -> List[Any]:
        app_list = super().get_app_list(request)
        #import ipdb; ipdb.set_trace()
        return list(filter(lambda x: x['app_label'] in self.include_apps, app_list))