from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from nossas.apps.basemodel import OnSiteBaseModel


class JobStatus(models.TextChoices):
    opened = "opened", _("Aberto")
    closed = "closed", _("Fechado")


class Job(OnSiteBaseModel):
    title = models.CharField(_("Título da vaga"), max_length=100)
    description = HTMLField(
        _("Descrição da vaga"), configuration="CKEDITOR_SETTINGS_JOB_MODEL"
    )
    picture = FilerImageField(
        verbose_name=_("Imagem"), on_delete=models.SET_NULL, blank=True, null=True
    )
    workload = models.CharField(_("Carga horária"), max_length=50)
    condition = models.CharField(_("Condições de trabalho"), max_length=50)
    responsibilities = HTMLField(
        _("Responsabilidades da vaga"), configuration="CKEDITOR_SETTINGS_JOB_MODEL"
    )
    prerequisites = HTMLField(
        _("Pré-requisitos da vaga"), configuration="CKEDITOR_SETTINGS_JOB_MODEL"
    )
    benefits = HTMLField(_("Benefícios"), configuration="CKEDITOR_SETTINGS_JOB_MODEL")
    salary_estimate = models.CharField(_("Estimativa salarial"), max_length=80)

    status = models.CharField(
        _("Status da vaga"),
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.opened,
    )

    created_at = models.DateTimeField(
        _("Data de criação"), auto_now_add=True, blank=True
    )

    class Meta:
        verbose_name = _("Vaga")
        verbose_name_plural = _("Vagas")

    def __str__(self):
        return self.title
