from django import forms
from django.db import transaction

from cms.forms.wizards import CreateCMSPageForm
from djangocms_text_ckeditor.widgets import TextEditorWidget

from contrib.bonde.widgets import BondeWidget

from .models import Pressure, SharingChoices


class CreatePressureForm(CreateCMSPageForm):
    content = None
    storytelling = forms.CharField(label="Narrativa", widget=TextEditorWidget)

    def get_template(self):
        return "campaign/modelo1.html"

    @transaction.atomic
    def save(self, content=None, **kwargs):
        from cms.api import add_plugin

        new_page = super(CreatePressureForm, self).save(**kwargs)
        new_page.rescan_placeholders()

        slot = "content"

        placeholder = self.get_placeholder(new_page, slot=slot)

        # Trabalhando bloco principal
        hero_block_plugin = add_plugin(
            placeholder=placeholder,
            plugin_type="BlockPlugin",
            language=self.language_code,
            title="Hero",
            slug="hero",
            background="#e40523",
        )

        # Trabalhando bloco de pressão
        pressure_block_plugin = add_plugin(
            placeholder=placeholder,
            plugin_type="GridBlockPlugin",
            language=self.language_code,
            title="Action",
            slug="action",
            background="black",
        )

        row_plugin = add_plugin(
            placeholder=placeholder,
            language=self.language_code,
            target=pressure_block_plugin,
            plugin_type="RowPlugin",
        )

        col_left_plugin = add_plugin(
            placeholder=placeholder,
            language=self.language_code,
            target=row_plugin,
            plugin_type="ColumnPlugin",
        )
        storytelling = self.cleaned_data.get("storytelling")
        add_plugin(
            placeholder=placeholder,
            language=self.language_code,
            target=col_left_plugin,
            plugin_type="TextPlugin",
            body=storytelling,
        )

        col_right_plugin = add_plugin(
            placeholder=placeholder,
            language=self.language_code,
            target=row_plugin,
            plugin_type="ColumnPlugin",
        )
        add_plugin(
            placeholder=placeholder,
            language=self.language_code,
            target=col_right_plugin,
            plugin_type="PressurePlugin",
        )

        # Trabalhando bloco de assinatura
        signature_block_plugin = add_plugin(
            placeholder=placeholder,
            plugin_type="BlockPlugin",
            language=self.language_code,
            title="Signature",
            slug="signature",
        )

        # content = self.cleaned_data.get("storytelling")
        # add_plugin(
        #     placeholder=placeholder,
        #     plugin_type="TextPlugin",
        #     language=self.language_code,
        #     target=hero_block_plugin,
        #     body=content
        # )

        return new_page

        # import ipdb;ipdb.set_trace()
        # Criar página padrão para tipo de form
        # pass


class PressureForm(forms.Form):
    # People Fields
    email_address = forms.EmailField(
        label="Endereço de email",
        widget=forms.EmailInput(attrs={"placeholder": "Insira seu e-mail"}),
    )

    given_name = forms.CharField(
        label="Primeiro nome",
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "Insira seu nome"}),
    )

    family_name = forms.CharField(
        label="Sobrenome",
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Insira seu sobrenome"}),
    )

    phone_number = forms.CharField(
        label="Whatsapp",
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "(DDD) 9 9999-9999"}),
    )

    # Action Fields
    email_subject = forms.CharField(label="Assunto", max_length=100, disabled=True)

    email_body = forms.CharField(
        label="Corpo do e-mail", disabled=True, widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(PressureForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = "input input-sm px-2 rounded-none hover:border-none focus:border-none focus:outline-none"

            if isinstance(visible.field.widget, forms.Textarea):
                visible.field.widget.attrs["class"] += " h-28"


class PressureSettingsForm(forms.ModelForm):
    # widget = forms.IntegerField(widget=forms.Select)

    is_group = forms.ChoiceField(
        label="Tipo",
        choices=((False, "Um grupo de alvos"), (True, "Mais de um grupo")),
        widget=forms.RadioSelect
    )

    sharing = forms.MultipleChoiceField(
        label="Opções de compartilhamento",
        choices=SharingChoices.choices,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Pressure
        # fields = "__all__"
        exclude = ["widget"]
