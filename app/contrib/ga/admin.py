from django.contrib import admin
from django.contrib.sites.models import Site

import admin2

from .models import GA


class GAInline(admin.StackedInline):
    model = GA
    can_delete = False

class SiteGAAdmin(admin2.ModelAdmin):
    inlines = (GAInline, )


admin2.site.unregister(Site)
admin2.site.register(Site, SiteGAAdmin)
