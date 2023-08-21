from django.contrib import admin

from .models import Candidate, PollingPlace, Voter


admin.site.register(PollingPlace)
admin.site.register(Candidate)
admin.site.register(Voter)