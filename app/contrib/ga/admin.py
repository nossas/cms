from django.contrib import admin
from django.contrib.sites.models import Site

from .models import GA

from contrib.designsystem.models import ThemeScss


class GAInline(admin.StackedInline):
    model = GA
    can_delete = False

class ThemeScssInline(admin.StackedInline):
    model = ThemeScss
    can_delete = False

class SiteGAAdmin(admin.ModelAdmin):
    inlines = (GAInline, ThemeScssInline, )


admin.site.unregister(Site)
admin.site.register(Site, SiteGAAdmin)
