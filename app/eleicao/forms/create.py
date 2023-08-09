from django import forms
from django_select2 import forms as s2forms
from django.forms.widgets import CheckboxInput

from ..models import Address, Candidate, Voter, PollingPlace

class CustomCheckboxInput(CheckboxInput):
    def __init__(self, *args, icon=None, text=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon
        self.text = text

class CustomBooleanField(forms.BooleanField):
    widget = CustomCheckboxInput

    def __init__(self, *args, icon=None, text=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.icon = icon
        self.widget.text = text

class Candidate1Form(forms.Form):
    agree = CustomBooleanField(required=True, icon='icon-children', text='Atuação em parceria permanente com serviços de proteção dos direitos da criança e do adolescente')
    agree_2 = CustomBooleanField(required=True, icon='icon-participate', text='Participação popular na construção de políticas públicas para crianças e adolescentes.')
    agree_3 = CustomBooleanField(required=True, icon='icon-religious-freedom', text='Respeito à liberdade religiosa, ao Estado laico e às diferentes religiosidades, com enfrentamento ativo ao racismo religioso.')
    agree_4 = CustomBooleanField(required=True, icon='icon-lgbt', text='Respeito aos direitos da população LGBT+, como o nome social de pessoas trans e a constituição de famílias homoparentais.')

    agree_5 = CustomBooleanField(required=True, icon='icon-network', text='Prioridade ao acionamento da rede de proteção, com encaminhamento a medidas socioeducativas como ultimo recurso')
    agree_6 = CustomBooleanField(required=True, icon='icon-family', text='Prioridade à manutenção dos vínculos familiares, com medida de abrigamento como último recurso (e sempre decidida com aval do Ministério Público).')
    agree_7 = CustomBooleanField(required=True, icon='icon-ears', text='Garantia de escuta especializada e depoimento especial para crianças e adolescentes em situação de violência.')
    agree_8 = CustomBooleanField(required=True, icon='icon-sexual-rights', text='Respeito aos direitos sexuais e reprodutivos e garantia de acesso ao aborto legal para crianças e adolescentes vítimas de violência sexual.')

    agree_9 = CustomBooleanField(required=True, icon='icon-indigenous', text='Efetivação dos direitos de populações indígenas e povos e comunidades tradicionais.')
    agree_10 = CustomBooleanField(required=True, icon='icon-plan', text='Planejamento de acordo com o Plano Decenal de Direitos Humanos de Crianças e Adolescentes.')
    agree_11 = CustomBooleanField(required=True, icon='icon-orcamento', text='Colaboração com o Poder Executivo local na elaboração do orçamento para crianças e adolescentes.')
    agree_12 = CustomBooleanField(required=True, icon='icon-sipia', text='Registro permanente de informações no SIPIA - Sistema de Informação para Infância e Adolescência.')

class Candidate2Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "email", "birth", "slug"]


class Candidate3Form(forms.ModelForm):
    class Meta:
        model = Candidate
        widgets = {
            "is_trans": forms.RadioSelect,
            "is_reelection": forms.RadioSelect
        }
        fields = [
            "occupation",
            "gender",
            "is_trans",
            "race",
            "is_reelection"
        ]

class Candidate4Form(forms.ModelForm):
    number = forms.IntegerField(label="Numero do candidato")
    # zone_id = forms.IntegerField()

    class Meta:
        model = Address
        fields = [
            "state",
            "city",
            "neighborhood",
            # "zone_id",
            "number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["state"].widget = s2forms.Select2Widget()
        self.fields["city"].widget = forms.Select()
        self.fields["neighborhood"].widget = forms.Select()
        # self.fields["zone_id"].widget = forms.Select()

class Candidate5Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["bio", "photo", "video", "social_media"]


class Candidate6Form(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["themes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["themes"].widget = forms.CheckboxSelectMultiple(
            choices=list(map(lambda x: x, Theme.objects.values_list("id", "label")))
        )


class PlacesWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "places__state__icontains",
        "places__city__icontains",
        "places__neighborhood__icontains",
    ]


class VoterForm(forms.ModelForm):
    zone = forms.ModelChoiceField(
        queryset=PollingPlace.objects.all(), label="Onde você vota?", required=True
    )

    class Meta:
        model = Voter
        fields = ["name", "email", "whatsapp", "zone"]
