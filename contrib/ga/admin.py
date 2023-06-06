from django.contrib import admin
from django.contrib.sites.models import Site

from .models import GA


class GAInline(admin.StackedInline):
    model = GA
    can_delete = False

class SiteGAAdmin(admin.ModelAdmin):
    inlines = (GAInline, )


admin.site.unregister(Site)
admin.site.register(Site, SiteGAAdmin)
