from django.contrib import admin

# Register your models here.
import admin2

from .models import (
    Mobilization,
    Widget,
    Community,
    DnsHostedZone,
    Block,
    CommunityUser,
    Theme,
    Subtheme,
    User,
)


class ThemeAdmin(admin2.ModelAdmin):
    list_display = ("id", "label", "value")
    list_filter = ("value", )

    # @admin.display
    # def get_mobilization__name(self, obj):
    #     return obj.mobilization.name


admin2.site.register(User)
admin2.site.register(Community)
admin2.site.register(CommunityUser)
admin2.site.register(DnsHostedZone)
admin2.site.register(Mobilization)
admin2.site.register(Block, admin2.ModelAdmin)
admin2.site.register(Widget)
admin2.site.register(Theme, ThemeAdmin)
admin2.site.register(Subtheme)
