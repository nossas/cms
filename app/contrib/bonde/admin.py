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

admin2.site.register(User)
admin2.site.register(Community)
admin2.site.register(CommunityUser)
admin2.site.register(DnsHostedZone)
admin2.site.register(Mobilization)
admin2.site.register(Block)
admin2.site.register(Widget)
admin2.site.register(Theme)
admin2.site.register(Subtheme)
