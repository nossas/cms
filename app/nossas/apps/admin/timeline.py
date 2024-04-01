from django.contrib import admin
from ..models.timeline import TimelineEvent

from nossas.apps.baseadmin import OnSiteAdmin

@admin.register(TimelineEvent)
class TimelineEventAdmin(OnSiteAdmin):
    list_display = ("title", "month", "year", "image")
    list_filter = ("year", "month")
    search_fields = ("title", "description")
