from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from cms.models import Page
from cms.models.fields import PlaceholderField
from filer.fields.image import FilerImageField
from tag_fields.managers import ModelTagsManager
from translated_fields import TranslatedField

# TODO: Mover esses imports para base de aplicativos e plugins
from nossas.apps.basemodel import OnSiteBaseModel


class Publication(OnSiteBaseModel):
    # Temporalidade
    created_at = models.DateTimeField(_("Data de criação"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Última atualização"), auto_now=True)

    # Conteúdo
    image_default = FilerImageField(
        verbose_name=_("Imagem Padrão"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    title = TranslatedField(
        models.CharField(_("Título"), max_length=180), {"en": {"blank": True}}
    )
    slug = models.SlugField(null=True, blank=True)
    description = TranslatedField(
        models.TextField(_("Descrição")), {"en": {"blank": True}}
    )
    external_link = models.URLField(
        verbose_name=_("Link externo"), null=True, blank=True
    )

    content = PlaceholderField("publication_content")

    # Classifação / Agrupamento
    parent = models.ForeignKey(
        Page,
        verbose_name=_("Página Relacionada"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = ModelTagsManager(blank=True)

    class Meta:
        verbose_name = _("Publicação")
        verbose_name_plural = _("Publicações")
        unique_together = ("slug", "parent", "site")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.external_link:
            return self.external_link

        if self.parent.application_namespace:
            return reverse(
                self.parent.application_namespace + ":detail",
                kwargs={"slug": self.slug},
            )

        return ""

    @property
    def get_pub_date(self):
        return self.created_at
