from django.contrib import admin
from django.contrib.sites.models import Site

from contrib.ga.admin import GAInline

from .models import Theme, SEO


class ThemeInline(admin.StackedInline):
    model = Theme
    can_delete = False


class SEOInline(admin.StackedInline):
    model = SEO
    can_delete = False


class SiteThemeAdmin(admin.ModelAdmin):
    inlines = (
        SEOInline,
        ThemeInline,
        GAInline,
    )


admin.site.unregister(Site)
admin.site.register(Site, SiteThemeAdmin)
