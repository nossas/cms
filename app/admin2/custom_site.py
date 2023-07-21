from django.contrib import admin


class AppSite(admin.AdminSite):
    site_header = "Monty Python administration"
    index_template = "admin2/index.html"