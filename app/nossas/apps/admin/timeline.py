from django.contrib import admin
from ..models.timeline import TimelineEvent

from nossas.apps.baseadmin import OnSiteAdmin
from ..forms.timeline import TimelineEventForm


@admin.register(TimelineEvent)
class TimelineEventAdmin(OnSiteAdmin):
    list_display = ("title", "month", "year", "image")
    list_filter = ("year", "month")
    search_fields = ("title", "description")
    form = TimelineEventForm
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "event_context",
                    ("day", "month", "year"),
                    "title",
                    "description",
                    "image",
                ],
            },
        ),
    )
