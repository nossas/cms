from django.contrib import admin

from .forms.register import RegisterAdminForm
from .models import Candidature, CandidatureFlow, ElectionResult
from .choices import PoliticalParty


class ElectionResultsInline(admin.StackedInline):
    model = ElectionResult
    extra = 1

class CandidatureAdmin(admin.ModelAdmin):
    search_fields = ("legal_name", "ballot_name", "email", "political_party")
    list_display = ("legal_name", "email", "political_party", "status", "updated_at")
    ordering = ("updated_at",)
    inlines = (ElectionResultsInline,)
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        for field in obj._meta.get_fields():
            if not field.is_relation:
                readonly_fields.append(field.name)
        return readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CandidatureFlowAdmin(admin.ModelAdmin):
    form = RegisterAdminForm
    change_form_template = "candidature/admin/change_form.html"
    search_fields = ["properties", ]
    list_filter = ("status",)
    list_display = (
        "legal_name",
        "email",
        "political_party",
        "status",
        "created_at",
        "updated_at",
    )
    ordering = ("-updated_at", "-created_at")

    fieldsets = (
        (None, {"fields": ("status", )}),
        (
            "Informações pessoais",
            {"fields": ("legal_name", ("cpf", "birth_date"), "email")},
        ),
        (
            "Dados de candidatura",
            {
                "fields": (
                    ("ballot_name", "number_id"),
                    ("intended_position", "political_party"),
                    "is_collective_mandate",
                    ("state", "city"),
                    ("deputy_mayor", "deputy_mayor_political_party"),
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
                ),
                "classes": ("proposes-fieldset", )
            }
        ),
        (
            "Trajetória",
            {
                "fields": (
                    ("education", "employment"),
                    "short_description",
                    "milestones"
                )
            }
        ),
        (
            "Complete seu perfil",
            {
                "fields": (
                    ("photo", "video"),
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
        return dict(PoliticalParty.choices).get(obj.properties.get("political_party"))

    def save_model(self, request, obj, form, change):
        # Força o formulário a passar novamente pelo processo de validação
        obj.status = "submitted"
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_search_results(self, request, queryset, search_term):
        from django.db.models import Q

        # Busca se o termo está presente em qualquer parte do campo JSON
        queryset = queryset.filter(
            Q(properties__icontains=search_term)
        )
        return queryset, False


admin.site.register(Candidature, CandidatureAdmin)
admin.site.register(CandidatureFlow, CandidatureFlowAdmin)
