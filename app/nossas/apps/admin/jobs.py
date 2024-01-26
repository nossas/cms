from django.contrib import admin

from nossas.apps.baseadmin import OnSiteAdmin
from ..models.jobs import Job


class JobAdmin(OnSiteAdmin):
    list_display = ("title", "status", "created_at")


admin.site.register(Job, JobAdmin)
