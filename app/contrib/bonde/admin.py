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


class ThemeAdmin2(admin2.ModelAdmin):
    list_display = ("id", "label", "value")
    list_filter = ("value", "label", )
    fields = ("value", ("label", "priority"))

    # @admin.display
    # def get_mobilization__name(self, obj):
    #     return obj.mobilization.name


class ThemeAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "value")
    list_filter = ("value", )


admin2.site.register(User, admin2.ModelAdmin)

admin2.site.register(Community, admin2.ModelAdmin)
admin.site.register(Community, admin.ModelAdmin)

admin2.site.register(CommunityUser, admin2.ModelAdmin)
admin2.site.register(DnsHostedZone, admin2.ModelAdmin)
admin2.site.register(Mobilization, admin2.ModelAdmin)
admin2.site.register(Block, admin2.ModelAdmin)
admin2.site.register(Widget, admin2.ModelAdmin)

admin2.site.register(Theme, ThemeAdmin2)
admin.site.register(Theme, ThemeAdmin)

admin2.site.register(Subtheme, admin2.ModelAdmin)
