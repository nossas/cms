from django.contrib import admin

from .models import Candidate, PollingPlace


admin.site.register(PollingPlace)
admin.site.register(Candidate)
