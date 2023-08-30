from django.contrib import admin

from .models import Candidate, PollingPlace, Voter


class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "get_place_city", "get_place_state")
    list_filter = ("place__state", )
    search_fields = ("name", "email")

    def get_place_city(self, obj):
        return obj.place.city

    get_place_city.short_description = "Cidade"

    def get_place_state(self, obj):
        return obj.place.state

    get_place_state.short_description = "Estado"


class PollingPlaceAdmin(admin.ModelAdmin):
    list_display = ("place", "city", "state")
    list_filter = ("state", )


admin.site.register(PollingPlace, PollingPlaceAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Voter)
