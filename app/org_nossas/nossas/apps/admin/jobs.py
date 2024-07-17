from django.contrib import admin

from org_nossas.nossas.apps.baseadmin import OnSiteAdmin
from ..models.jobs import Job


class JobAdmin(OnSiteAdmin):
    list_display = ("title", "status", "created_at")


admin.site.register(Job, JobAdmin)
