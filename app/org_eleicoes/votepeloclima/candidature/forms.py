from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

from captcha.widgets import ReCaptchaV2Checkbox

from .fields import ValidateOnceReCaptchaField, StateCepField, CityCepField


class DisabledMixin:

    def __init__(self, disabled=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if disabled:
            # import ipdb;ipdb.set_trace()
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {"readonly": True, "disabled": True}
                )


class CaptchaForm(forms.Form):
    captcha = ValidateOnceReCaptchaField(widget=ReCaptchaV2Checkbox())


class InitialForm(DisabledMixin, forms.Form):
    legal_name = forms.CharField(label=_("Nome"))
    ballot_name = forms.CharField(label=_("Nome na urna"))
    birth_date = forms.DateField(label=_("Data de nascimento"))
    email = forms.EmailField(label=_("E-mail"))
    cpf_cnpj = forms.CharField(label=_("CPF/CNPJ"))
    tse_id = forms.CharField(label=_("Identificação TSE (?)"), required=False)

    class Meta:
        title = _("Informações iniciais")


class ApplicationForm(DisabledMixin, forms.Form):
    number_id = forms.IntegerField(label=_("Número de identificação"), min_value=1)
    intended_position = forms.CharField(label=_("Cargo pretendido"))
    state = StateCepField(label=_("Estado"))
    city = CityCepField(label=_("Cidade"))
    is_collective_mandate = forms.BooleanField(
        label=_("É um mandato coletivo?"), required=False
    )
    political_party = forms.CharField(label=_("Partido político"))
    
    class Meta:
        title = _("Informações de candidatura")


class ProfileForm(DisabledMixin, forms.Form):
    video = forms.FileField(label=_("Vídeo"), required=False)
    photo = forms.FileField(label=_("Foto"), required=False)
    gender = forms.CharField(label=_("Gênero"))
    color = forms.CharField(label=_("Raça"))
    sexuality = forms.CharField(label=_("Sexualidade"), required=False)

    class Meta:
        title = _("Complemente seu perfil")


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
    
    def clean_photo(self):
        content = self.cleaned_data["photo"]
        if content:
            if content.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
                raise forms.ValidationError(
                    _(
                        "Somente são aceitos arquivos em PNG ou JPEG. Selecione outra imagem, por favor."
                    )
                )

        return content


class TrackForm(DisabledMixin, forms.Form):
    education = forms.CharField(label=_("Escolaridade"), required=False)
    employment = forms.CharField(label=_("Ocupação"), required=False)
    short_description = forms.CharField(label=_("Minibio"), widget=forms.Textarea())

    class Meta:
        title = _("Sobre sua trajetória")


class FlagForm(DisabledMixin, forms.Form):
    is_renewable_energy = forms.BooleanField(label=_("Energia Renovável"), required=False)
    is_transport_and_mobility = forms.BooleanField(
        label=_("Transporte e Mobilidade"), required=False
    )

    class Meta:
        title = _("Bandeiras da sua candidatura")


class AppointmentForm(DisabledMixin, forms.Form):
    appointment_1 = forms.BooleanField(label=_("Compromisso 1"), required=False)
    appointment_2 = forms.BooleanField(label=_("Compromisso 2"), required=False)

    class Meta:
        title = _("Você assume compromisso com...")


class CheckoutForm(forms.Form):
    is_valid = forms.BooleanField()

    class Meta:
        title = _("Para finalizar, confirme as suas informações")


register_form_list = [
    ("captcha", CaptchaForm),
    ("compromissos", AppointmentForm),
    ("informacoes-iniciais", InitialForm),
    ("informacoes-de-candidatura", ApplicationForm),
    ("complemente-seu-perfil", ProfileForm),
    ("sobre-sua-trajetoria", TrackForm),
    ("bandeiras-da-sua-candidatura", FlagForm),
    ("checkout", CheckoutForm),
]
