from django import forms
from django.utils.translation import ugettext_lazy as _

# from django_jsonform.forms.fields import JSONFormField

from cms.plugin_pool import plugin_pool

from djangocms_form_builder.models import Form
from djangocms_form_builder.cms_plugins import FormPlugin as FormPluginBase
from djangocms_form_builder.forms import FormsForm as FormsFormBase
from djangocms_text_ckeditor.fields import HTMLFormField

from .models import FormProxy


plugin_pool.unregister_plugin(FormPluginBase)


class FormsForm(FormsFormBase):
    submit_text = forms.CharField(
        label=_("Botão enviar"), required=False, initial=_("Enviar")
    )
    success_message = HTMLFormField(label=_("Mensagem de sucesso"))

    class Meta:
        model = Form
        exclude = ()
        untangled_fields = [
            "form_selection",
            "form_name",
            "form_login_required",
            "form_unique",
            "form_floating_labels",
            "form_spacing",
            "form_actions",
            "attributes",
            "captcha_widget",
            "captcha_requirement",
            "captcha_config",
        ]
        entangled_fields = {
            "action_parameters": [],
            "extra_config": ["submit_text", "success_message"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha_widget"].initial = ""


@plugin_pool.register_plugin
class FormPlugin(FormPluginBase):
    name = _("Formulário")
    model = FormProxy
    form = FormsForm
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "form_selection",
                    "form_name",
                    "submit_text",
                    "success_message",
                ],
            },
        ),
    ]
