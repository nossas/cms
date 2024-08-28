from django.contrib import admin
from django import forms

from .models import Candidature, CandidatureFlow


class CandidatureAdmin(admin.ModelAdmin):
    search_fields = ("legal_name", "ballot_name", "email", "political_party")
    list_display = ("legal_name", "email", "political_party", "status")

    def has_add_permission(self, request):
        return False


class CandidatureFlowAdminForm(forms.ModelForm):
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
        fields = [
            'photo', 'video', 'status',
            'legal_name', 'cpf', 'email', 'birth_date',
            'ballot_name', 'number_id', 'intended_position', 'state', 'city',
            'political_party', 'deputy_mayor', 'deputy_mayor_political_party'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar os campos do formulário com os valores do JSON `properties`
        if self.instance and self.instance.properties:
            props = self.instance.properties
            self.fields['legal_name'].initial = props.get('legal_name', '')
            self.fields['cpf'].initial = props.get('cpf', '')
            self.fields['email'].initial = props.get('email', '')
            self.fields['birth_date'].initial = props.get('birth_date', '')
            self.fields['ballot_name'].initial = props.get('ballot_name', '')
            self.fields['number_id'].initial = props.get('number_id', '')
            self.fields['intended_position'].initial = props.get('intended_position', '')
            self.fields['state'].initial = props.get('state', '')
            self.fields['city'].initial = props.get('city', '')
            self.fields['political_party'].initial = props.get('political_party', '')
            self.fields['deputy_mayor'].initial = props.get('deputy_mayor', '')
            self.fields['deputy_mayor_political_party'].initial = props.get('deputy_mayor_political_party', '')

    def save(self, commit=True):
        instance = super().save(commit=False)
        properties = instance.properties or {}

        # Atualizar o JSON `properties` com os dados do formulário
        properties['legal_name'] = self.cleaned_data.get('legal_name')
        properties['cpf'] = self.cleaned_data.get('cpf')
        properties['email'] = self.cleaned_data.get('email')
        properties['birth_date'] = self.cleaned_data.get('birth_date')
        properties['ballot_name'] = self.cleaned_data.get('ballot_name')
        properties['number_id'] = self.cleaned_data.get('number_id')
        properties['intended_position'] = self.cleaned_data.get('intended_position')
        properties['state'] = self.cleaned_data.get('state')
        properties['city'] = self.cleaned_data.get('city')
        properties['political_party'] = self.cleaned_data.get('political_party')
        properties['deputy_mayor'] = self.cleaned_data.get('deputy_mayor')
        properties['deputy_mayor_political_party'] = self.cleaned_data.get('deputy_mayor_political_party')

        instance.properties = properties
        if commit:
            instance.save()
        return instance

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