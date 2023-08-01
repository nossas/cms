from django.contrib import admin

from .models import Candidate, Theme, PollingPlace


admin.site.register(Theme)
admin.site.register(PollingPlace)
admin.site.register(Candidate)