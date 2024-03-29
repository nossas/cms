from django.contrib import admin
from django.http.request import HttpRequest

from django.utils.html import format_html


from .models import VPS, HostedZone, RecordSet


class VPSAdmin(admin.ModelAdmin):
    list_display = ("name", "static_ip")
    # list_filter = ("name", )

admin.site.register(VPS, VPSAdmin)


class RecordSetAdmin(admin.ModelAdmin):
    search_fields = ("name", )


admin.site.register(RecordSet, RecordSetAdmin)


class RecordSetInline(admin.TabularInline):
    model = RecordSet
    extra = 0


class HostedZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "vps", "healtcheck")
    search_fields = ("name", )
    list_filter = ("healtcheck", )
    readonly_fields = ("healtcheck", )
    inlines = [RecordSetInline, ]

    class Media:
        css = {
             'all': ('css/route53/tags.css',)
        }
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_superuser:
            return False
        
        return super(HostedZoneAdmin, self).has_add_permission(request)

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if not request.user.is_superuser:
            return False
        
        return super(HostedZoneAdmin, self).has_change_permission(request, obj=obj)

    def vps(self, obj):
        html = "<ul class='tags'>"
        for x in obj.related_instances():
            html += "<li>" + x.name + "</li>"
        html += "</ul>"
        
        return format_html(html)


admin.site.register(HostedZone, HostedZoneAdmin)