from django.contrib import admin

from .models import Site


class SiteAdmin(admin.ModelAdmin):
    list_display = ("dns", "subdomain", "instance", "service")
    autocomplete_fields = ("dns", "subdomain")


admin.site.register(Site, SiteAdmin)