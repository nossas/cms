from django.contrib import admin


class AppSite(admin.AdminSite):
    site_header = "Admin2"
    index_template = "admin2/index.html"