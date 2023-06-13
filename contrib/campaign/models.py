from django.db import models

from cms.models import CMSPlugin


class Thank(models.Model):
    # Agradecimento
    thank_email_subject = models.CharField(
        verbose_name="Assunto do e-mail de agradecimento para quem vai pressionar",
        max_length=120,
    )
    thank_email_body = models.TextField(verbose_name="Corpo do e-mail de agradecimento")
    sender_name = models.CharField(verbose_name="Remetente", max_length=120)
    sender_email = models.EmailField(verbose_name="Email de resposta")

    class Meta:
        abstract = True


class SharingChoices(models.TextChoices):
    whatsapp = "whatsapp", "Whatsapp"
    twitter = "twitter", "Twitter"
    facebook = "facebook", "Facebook"


class PostAction(models.Model):
    # Pós ação
    sharing = models.JSONField(
        verbose_name="Opções de compartilhamento",
        # choices=SharingChoices.choices,
        # max_length=50,
    )
    whatsapp_text = models.TextField(verbose_name="Mensagem para o whatsapp")

    class Meta:
        abstract = True


class Target(models.Model):
    name = models.CharField(verbose_name="Nome do alvo", max_length=100)
    email = models.EmailField(
        verbose_name="Email do alvo", max_length=100, null=True, blank=True
    )
    phone = models.CharField(
        verbose_name="Telefone do alvo", max_length=20, null=True, blank=True
    )

    class Meta:
        verbose_name ="Alvo"
        verbose_name_plural = "Alvos"
    

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Pressure(PostAction, Thank, CMSPlugin):
    widget = models.IntegerField(null=True, blank=True)

    email_subject = models.JSONField(
        verbose_name="Assunto do e-mail para os alvos"
    )
    email_body = models.TextField(
        verbose_name="Corpo do e-mail para os alvos"
    )

    # Envio
    submissions_limit = models.IntegerField(
        verbose_name="Limite de envios únicos", null=True, blank=True
    )
    submissions_interval = models.IntegerField(
        verbose_name="Intervalo de envio", null=True, blank=True
    )

    disable_editing = models.BooleanField(
        verbose_name="Desabilitar edição do e-mail e do assunto pelos ativistas?",
        default=True,
    )

    def copy_relations(self, old_instance):
        # https://docs.django-cms.org/en/latest/how_to/custom_plugins.html#handling-relations
        self.targetgroup_set.set(old_instance.targetgroup_set.all())


class TargetGroup(models.Model):
    name = models.CharField(verbose_name="Nome do grupo", max_length=50)
    targets = models.ManyToManyField(Target, verbose_name="Alvos")

    pressure = models.ForeignKey(Pressure, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Grupo de alvos"
        verbose_name_plural = "Grupos de alvos"
