from django import forms

# from django.contrib import admin

# Register your models here.

from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template

from djangocms_form_builder import actions

from .api import create_form_entry


@actions.register
class IntegrateWithBonde(actions.FormAction):
    verbose_name = _("Integração com o BONDE")

    class Meta:
        entangled_fields = {
            "action_parameters": ["cached_community_id", "mobilization_id", "widget_id"]
        }

    cached_community_id = forms.IntegerField(label="ID da Comunidade", required=False)
    mobilization_id = forms.IntegerField(label="ID da Mobilização", required=False)
    widget_id = forms.IntegerField(label="ID da Widget", required=False)

    def execute(self, form, request):
        # Integração com o BONDE
        settings = {
            "cached_community_id": self.get_parameter(form, "cached_community_id"),
            "mobilization_id": self.get_parameter(form, "mobilization_id"),
            "widget_id": self.get_parameter(form, "widget_id"),
        }

        if len(list(filter(lambda x: not x, settings.values()))) == 0:
            create_form_entry(settings, **form.cleaned_data)



@actions.register
class IntegrateWithEmail(actions.FormAction):
    verbose_name = _("Integração com o EMAIL")

    class Meta:
        entangled_fields = {
            "action_parameters": ["subject", "to_email"]
        }
    
    # name = forms.CharField(label="Nome", required=False)
    to_email = forms.EmailField(label="Email", required=False)
    subject = forms.CharField(label="Assunto", required=False)
    body = forms.CharField(label="Corpo do e-mail", required=False, widget=forms.Textarea)

    def execute(self, form, request):
        # name = self.get_parameter(form, "name")
        to_email = self.get_parameter(form, "to_email")
        subject_text = self.get_parameter(form, "subject")
        body_text = self.get_parameter(form, "body")

        # context = form.cleaned_data
        # email_template_name = "forms/body.html"
        # html_email_template_name = email_template_name
        # import ipdb;ipdb.set_trace()
        # if to_email and body_text and subject_text:
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        from_email = form.cleaned_data.get("email")
        context = Context({**form.cleaned_data})
        # subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        # subject = "".join(subject.splitlines())

        subject = Template(subject_text).render(context)
        body = Template(body_text).render(context)


        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(body, "text/html")
        email_message.send()

# TODO:
# Adicionar campos do formulário no contexto do assunto
# 