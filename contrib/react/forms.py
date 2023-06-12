from django import forms

from contrib.campaign.models import SharingChoices
from tailwind.fields import InputArrayField
from tailwind.widgets import RadioSelect, CheckboxSelectMultiple

from .models import Email



class BaseForm(forms.ModelForm):

    def save(self, commit: bool):
        if hasattr(self, "cleaned_data"):
            print(self.cleaned_data)
        # import ipdb;ipdb.set_trace()
        # print("BaseForm.save ->>", self.cleaned_data)
        pass


class TargetsForm(BaseForm):
    targets_type = forms.ChoiceField(
        label="Tipo",
        choices=((True, "Um grupo de alvos"), (False, "Mais de um grupo de alvos")),
        widget=RadioSelect,
        initial=True,
    )
    targets = InputArrayField(label="Alvos", num_widgets=10)

    class Meta:
        model = Email
        fields = ["targets_type"]


class EmailForm(BaseForm):
    email_subject = InputArrayField(
        label="Assunto do e-mail para os alvos", num_widgets=10
    )

    email_body = forms.CharField(
        label="Corpo do e-mail para os alvos", widget=forms.Textarea
    )

    disable_editing = forms.ChoiceField(
        label="Desabilitar edição do e-mail e do assunto pelos ativistas?",
        choices=((True, "Desabilitar"), (False, "Habilitar")),
        widget=RadioSelect,
        initial=True,
    )

    class Meta:
        model = Email
        fields = ["email_subject", "email_body", "disable_editing"]


class SendForm(BaseForm):
    submissions_limit = forms.ChoiceField(
        label="Limite de envios únicos",
        choices=(
            (500, "500 pressões"),
            (1000, "1.000 pressões"),
            (5000, "5.000 pressões"),
            (10000, "10.000 pressões"),
        ),
    )

    submissions_interval = forms.ChoiceField(
        label="Intervalo de envio",
        choices=(
            (50, "A cada 50 pressões"),
            (100, "A cada 100 pressões"),
            (500, "A cada 500 pressões"),
            (1000, "A cada 1.000 pressões"),
        ),
    )

    class Meta:
        model = Email
        fields = ["submissions_limit", "submissions_interval"]


class ThankForm(BaseForm):
    thank_email_subject = forms.CharField(
        label="Assunto do e-mail de agradecimento para quem vai pressionar",
        max_length=120,
    )
    thank_email_body = forms.CharField(
        label="Corpo do e-mail de agradecimento", widget=forms.Textarea
    )
    sender_name = forms.CharField(label="Remetente", max_length=120)
    sender_email = forms.EmailField(label="Email de resposta")

    class Meta:
        model = Email
        fields = [
            "thank_email_subject",
            "sender_name",
            "sender_email",
            "thank_email_body",
        ]


class PostActionForm(BaseForm):
    sharing = forms.MultipleChoiceField(
        label="Opções de compartilhamento",
        choices=SharingChoices.choices,
        widget=CheckboxSelectMultiple,
    )
    whatsapp_text = forms.CharField(
        label="Mensagem para o whatsapp", widget=forms.Textarea
    )

    class Meta:
        model = Email
        fields = [
            "sharing",
            "whatsapp_text"
        ]
