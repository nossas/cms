from django.contrib import admin

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

    def vps(self, obj):
        html = "<ul class='tags'>"
        for x in obj.related_instances():
            html += "<li>" + x.name + "</li>"
        html += "</ul>"
        
        return format_html(html)


admin.site.register(HostedZone, HostedZoneAdmin)