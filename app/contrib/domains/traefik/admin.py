from django.contrib import admin

from .models import Route


class RouteAdmin(admin.ModelAdmin):
    list_display = ("dns", "subdomain", "instance", "service")
    autocomplete_fields = ("dns", "subdomain")


admin.site.register(Route, RouteAdmin)