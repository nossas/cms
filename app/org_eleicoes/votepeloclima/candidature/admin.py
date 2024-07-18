from django.contrib import admin

from .models import Candidature, CandidatureFlow


class CandidatureAdmin(admin.ModelAdmin):
    search_fields = ("legal_name", "ballot_name", "email", "political_party")
    list_display = ("legal_name", "email", "political_party", "status")

    def has_add_permission(self, request):
        return False


class CandidatureFlowAdmin(admin.ModelAdmin):
    list_filter = ("status", )
    list_display = ("legal_name", "email", "political_party", "status")

    @admin.display
    def legal_name(self, obj):
        return obj.properties.get("informacoes-iniciais-legal_name")
    
    @admin.display
    def email(self, obj):
        return obj.properties.get("informacoes-iniciais-email")
    
    @admin.display
    def political_party(self, obj):
        return obj.properties.get("informacoes-de-candidatura-political_party")
    
    def has_add_permission(self, request):
        return False


admin.site.register(Candidature, CandidatureAdmin)
admin.site.register(CandidatureFlow, CandidatureFlowAdmin)