from django.contrib import admin


class AppSite(admin.AdminSite):
    site_header = "Admin2"
    index_template = "admin2/index.html"
    app_index_template = "admin2/app_index.html"