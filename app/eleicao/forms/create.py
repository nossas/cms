from django import forms
from django_select2 import forms as s2forms
from django.forms.widgets import CheckboxInput
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from .widgets import SocialMedia
from ..models import Address, Candidate, Voter, PollingPlace


class IconCheckboxInput(CheckboxInput):
    def __init__(self, *args, icon=None, text=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon


class IconBooleanField(forms.BooleanField):
    widget = IconCheckboxInput

    def __init__(self, *args, icon=None, text=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.icon = icon


class Candidate1Form(forms.Form):
    title = "Oi, Candidata(o)"
    starter_text = "Em todo o Brasil existem milhares de pessoas que se dedicam ao trabalho nos Conselhos Tutelares para fazer valer os direitos de crianças e adolescentes - a importante e necessária missão de ser conselheiro e conselheira tutelar! Criamos uma plataforma para destacar essas candidaturas e conectá-las aos eleitores da sua região."


class Candidate2Form(forms.Form):
    title = "Você assume compromisso com..."
    agree = IconBooleanField(
        label="Atuação em parceria permanente com serviços de proteção dos direitos da criança e do adolescente",
        required=True,
        icon="icon-children"
    )
    agree_2 = IconBooleanField(
        label="Participação popular na construção de políticas públicas para crianças e adolescentes.",
        required=True,
        icon="icon-participate"
    )
    agree_3 = IconBooleanField(
        label="Respeito à liberdade religiosa, ao Estado laico e às diferentes religiosidades, com enfrentamento ativo ao racismo religioso.",
        required=True,
        icon="icon-religious-freedom"
    )
    agree_4 = IconBooleanField(
        label="Respeito aos direitos da população LGBT+, como o nome social de pessoas trans e a constituição de famílias homoparentais.",
        required=True,
        icon="icon-lgbt"
    )
    agree_5 = IconBooleanField(
        label="Prioridade ao acionamento da rede de proteção, com encaminhamento a medidas socioeducativas como ultimo recurso",
        required=True,
        icon="icon-network",
    )
    agree_6 = IconBooleanField(
        label="Prioridade à manutenção dos vínculos familiares, com medida de abrigamento como último recurso (e sempre decidida com aval do Ministério Público).",
        required=True,
        icon="icon-family",
    )


class Candidate3Form(forms.Form):
    title = "Você assume compromisso com..."
    agree_7 = IconBooleanField(
        label="Garantia de escuta especializada e depoimento especial para crianças e adolescentes em situação de violência.",
        required=True,
        icon="icon-ears",
    )
    agree_8 = IconBooleanField(
        label="Respeito aos direitos sexuais e reprodutivos e garantia de acesso ao aborto legal para crianças e adolescentes vítimas de violência sexual.",
        required=True,
        icon="icon-sexual-rights",
    )
    agree_9 = IconBooleanField(
        label="Efetivação dos direitos de populações indígenas e povos e comunidades tradicionais.",
        required=True,
        icon="icon-indigenous",
    )
    agree_10 = IconBooleanField(
        label="Planejamento de acordo com o Plano Decenal de Direitos Humanos de Crianças e Adolescentes.",
        required=True,
        icon="icon-plan",
    )
    agree_11 = IconBooleanField(
        label="Colaboração com o Poder Executivo local na elaboração do orçamento para crianças e adolescentes.",
        required=True,
        icon="icon-orcamento",
    )
    agree_12 = IconBooleanField(
        label="Registro permanente de informações no SIPIA - Sistema de Informação para Infância e Adolescência.",
        required=True,
        icon="icon-sipia",
    )


class Candidate4Form(forms.ModelForm):
    title = "Seus dados"

    class Meta:
        model = Candidate
        fields = ["name", "email", "birth", "slug", "newsletter"]
        widgets = {
            "name": forms.TextInput({"placeholder": "Seu nome"}),
            "birth": forms.DateInput(
                format="%d-%m-%Y",
                attrs={
                    "class": "date",
                    "data-mask": "00/00/0000",
                    "placeholder": "DD/MM/AAAA",
                },
            ),
            "email": forms.EmailInput({"placeholder": "Seu email"}),
            "slug": forms.TextInput({"placeholder": "seunome"})
        }


class Candidate5Form(forms.ModelForm):
    title = "Seus dados"

    class Meta:
        model = Candidate
        widgets = {
            "is_trans": forms.RadioSelect(attrs={"class": "radio-select"}),
            "occupation": forms.TextInput({"placeholder": "Digite sua profissão"}),
        }
        fields = ["occupation", "gender", "is_trans", "race"]


class Candidate6Form(forms.ModelForm):
    title = "Sua candidatura"

    number = forms.IntegerField(
        label="Numero do candidato",
        widget=forms.TextInput({"placeholder": "Seu número de voto"}),
    )
    is_reelection = forms.BooleanField(
        label="Está se candidatando para reeleição?",
        required=False,
        initial=False,
        widget=forms.RadioSelect(
            choices=((True, "Sim"), (False, "Não")),
            attrs={"class": "radio-select"}
        ),
    )

    class Meta:
        model = Address
        fields = ["state", "city", "neighborhood", "number", "is_reelection"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["city"].widget = forms.Select()
        self.fields["neighborhood"].widget = forms.Select()


class Candidate7Form(forms.ModelForm):
    title = "Complemente seu perfil"

    class Meta:
        model = Candidate
        fields = ["bio", "photo", "video", "social_media"]
        widgets = {
            "bio": forms.Textarea(
                {
                    "placeholder": "Em um parágrafo, o que os(as) eleitores(as) precisam saber sobre você."
                }
            ),
            "social_media": SocialMedia(),
        }

    def clean_video(self):
        content = self.cleaned_data["video"]
        # 50MB
        max_size = 52428800
        if content:
            if "video" in content.content_type:
                if content.size > max_size:
                    raise forms.ValidationError(
                        _(
                            "Por favor, escolha um video com tamanho de até %s. Tamanho Atual %s"
                        )
                        % (filesizeformat(max_size), filesizeformat(content.size))
                    )
            else:
                raise forms.ValidationError(_("Tipo de arquivo não suportado."))
        return content


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
