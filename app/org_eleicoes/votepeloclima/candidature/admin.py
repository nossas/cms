from django.contrib import admin
from django import forms
from entangled.forms import EntangledModelForm

from .models import Candidature, CandidatureFlow


class CandidatureAdmin(admin.ModelAdmin):
    search_fields = ("legal_name", "ballot_name", "email", "political_party")
    list_display = ("legal_name", "email", "political_party", "status")

    def has_add_permission(self, request):
        return False


class CandidatureFlowAdminForm(EntangledModelForm):
    legal_name = forms.CharField(label='Nome Legal', required=True)
    cpf = forms.CharField(label='CPF', required=True)
    email = forms.EmailField(label='Email', required=True)
    birth_date = forms.DateField(
        label='Data de Nascimento', 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    ballot_name = forms.CharField(label='Nome na Urna', required=True)
    number_id = forms.CharField(label='Número de Identificação', required=True)
    intended_position = forms.CharField(label='Cargo Pretendido', required=True)
    state = forms.CharField(label='Estado', required=True)
    city = forms.CharField(label='Cidade', required=True)
    political_party = forms.CharField(label='Partido Político', required=True)
    deputy_mayor = forms.CharField(label='Vice-prefeito', required=False)
    deputy_mayor_political_party = forms.CharField(label='Partido do Vice-prefeito', required=False)

    class Meta:
        model = CandidatureFlow
        entangled_fields = {'properties': [
            'legal_name', 'cpf', 'email', 'birth_date', 
            'ballot_name', 'number_id', 'intended_position', 
            'state', 'city', 'political_party', 
            'deputy_mayor', 'deputy_mayor_political_party'
        ]}
        untangled_fields = ['photo', 'video', 'status']


class CandidatureFlowAdmin(admin.ModelAdmin):
    form = CandidatureFlowAdminForm
    list_filter = ("status", )
    list_display = ("legal_name", "email", "political_party", "status")
    
    fieldsets = (
        (None, {
            'fields': ('photo', 'video', 'status')
        }),
        ('Informações Pessoais', {
            'fields': (
                'legal_name', 
                'cpf', 
                'email', 
                'birth_date'
            )
        }),
        ('Dados de Candidatura', {
            'fields': (
                'ballot_name', 
                'number_id',
                'intended_position',
                'state', 
                'city', 
                'political_party', 
                'deputy_mayor', 
                'deputy_mayor_political_party'
            )
        }),
    )

    @admin.display
    def legal_name(self, obj):
        return obj.properties.get("legal_name")
    
    @admin.display
    def email(self, obj):
        return obj.properties.get("email")
    
    @admin.display
    def political_party(self, obj):
        return obj.properties.get("political_party")
    
    def has_add_permission(self, request):
        return False


admin.site.register(Candidature, CandidatureAdmin)
admin.site.register(CandidatureFlow, CandidatureFlowAdmin)