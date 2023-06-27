from django.db import models

from cms.models import CMSPlugin
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from filer.fields.image import FilerImageField


# class Thank(models.Model):
#     # Agradecimento
#     thank_email_subject = models.CharField(
#         verbose_name="Assunto do e-mail de agradecimento para quem vai pressionar",
#         max_length=120,
#         blank=True,
#         null=True,
#     )
#     thank_email_body = models.TextField(
#         verbose_name="Corpo do e-mail de agradecimento", blank=True, null=True
#     )
#     sender_name = models.CharField(
#         verbose_name="Remetente", max_length=120, blank=True, null=True
#     )
#     sender_email = models.EmailField(
#         verbose_name="Email de resposta", blank=True, null=True
#     )

#     class Meta:
#         abstract = True


# class SharingChoices(models.TextChoices):
#     whatsapp = "whatsapp", "Whatsapp"
#     twitter = "twitter", "Twitter"
#     facebook = "facebook", "Facebook"


# class PostAction(models.Model):
#     # Pós ação
#     sharing = models.JSONField(
#         verbose_name="Opções de compartilhamento", blank=True, null=True
#     )
#     whatsapp_text = models.TextField(
#         verbose_name="Mensagem para o whatsapp", blank=True, null=True
#     )

#     class Meta:
#         abstract = True


# class Pressure(PostAction, Thank, CMSPlugin):
#     widget = models.IntegerField(null=True, blank=True)
#     targets = models.JSONField(verbose_name="Alvos", null=True, blank=True)

#     email_subject = models.JSONField(verbose_name="Assunto do e-mail para os alvos")
#     email_body = models.TextField(verbose_name="Corpo do e-mail para os alvos")

#     # Envio
#     submissions_limit = models.IntegerField(
#         verbose_name="Limite de envios únicos", null=True, blank=True
#     )
#     submissions_interval = models.IntegerField(
#         verbose_name="Intervalo de envio", null=True, blank=True
#     )

#     disable_editing = models.BooleanField(
#         verbose_name="Desabilitar edição do e-mail e do assunto pelos ativistas?",
#         default=True,
#     )


class Pressure(CMSPlugin):
    widget_id = models.IntegerField(null=True, blank=True)


class IconExtension(PageExtension):
    favicon = FilerImageField(
        verbose_name="Favicon",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )


extension_pool.register(IconExtension)
