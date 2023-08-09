from django.contrib import admin

from .models import Candidate, PollingPlace, Address


admin.site.register(PollingPlace)
admin.site.register(Candidate)
admin.site.register(Address)
