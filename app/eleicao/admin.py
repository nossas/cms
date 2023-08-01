from django.contrib import admin

from .models import Candidate, Theme, PollingPlace, Address


admin.site.register(Theme)
admin.site.register(PollingPlace)
admin.site.register(Candidate)
admin.site.register(Address)