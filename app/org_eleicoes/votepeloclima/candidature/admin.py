from typing import Any
from django.contrib import admin
from django import forms
from django.http import HttpRequest
from entangled.forms import EntangledModelForm

from .forms.register import RegisterAdminForm
from .models import Candidature, CandidatureFlow


class CandidatureAdmin(admin.ModelAdmin):
    search_fields = ("legal_name", "ballot_name", "email", "political_party")
    list_display = ("legal_name", "email", "political_party", "status", "updated_at")
    ordering = ("updated_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CandidatureFlowAdmin(admin.ModelAdmin):
    form = RegisterAdminForm
    list_filter = ("status",)
    list_display = (
        "legal_name",
        "email",
        "political_party",
        "status",
        "created_at",
        "updated_at",
    )
    ordering = ("updated_at",)

    fieldsets = (
        (None, {"fields": ("status", )}),
        (
            "Informações pessoais",
            {"fields": ("legal_name", "cpf", "email", "birth_date")},
        ),
        (
            "Dados de candidatura",
            {
                "fields": (
                    "ballot_name",
                    "number_id",
                    "intended_position",
                    "state",
                    "city",
                    "is_collective_mandate",
                    "political_party",
                    "deputy_mayor",
                    "deputy_mayor_political_party",
                )
            },
        ),
        (
            "Propostas",
            {
                "fields": (
                    "transporte_e_mobilidade",
                    "gestao_de_residuos",
                    "povos_originarios_tradicionais",
                    "educacao_climatica",
                    "combate_racismo_ambiental",
                    "moradia_digna",
                    "transicao_energetica",
                    "agricultura_sustentavel",
                    "direito_a_cidade",
                    "adaptacao_reducao_desastres",
                    "direito_dos_animais",
                    "economia_verde",
                    "pessoas_afetadas_desastres"
                )
            }
        ),
        (
            "Trajetória",
            {
                "fields": (
                    "education",
                    "employment",
                    "short_description",
                    "milestones"
                )
            }
        ),
        (
            "Complete seu perfil",
            {
                "fields": (
                    "photo",
                    "video",
                    "gender",
                    "color",
                    "sexuality",
                    "social_media"
                )
            }
        )
    )

    readonly_fields = ("status", "photo", "video")

    class Media:
        css = {"all": ("css/candidature/admin.css",)}

    @admin.display
    def legal_name(self, obj):
        return obj.properties.get("legal_name")

    @admin.display
    def email(self, obj):
        return obj.properties.get("email")

    @admin.display
    def political_party(self, obj):
        return obj.properties.get("political_party")

    @admin.display
    def cpf(self, obj):
        return obj.properties.get("cpf")

    def save_form(self, request: HttpRequest, form: forms.ModelForm, change: bool) -> Any:
        # import ipdb;ipdb.set_trace()
        raise Exception("Desabilitado alterar formulário")
        # return super().save_form(request, form, change)

    def save_model(self, request: HttpRequest, obj: Any, form: forms.ModelForm, change: bool) -> None:
        # import ipdb;ipdb.set_trace()
        raise Exception("Desabilitado alterar formulário")
        # return super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Candidature, CandidatureAdmin)
admin.site.register(CandidatureFlow, CandidatureFlowAdmin)
