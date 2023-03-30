from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin

from autoslug import AutoSlugField

# Create your models here.
class Content(CMSPlugin):
    name = models.CharField(verbose_name=_('name'), max_length=30)
    slug = AutoSlugField(populate_from='name')
    
    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('contents')
        ordering = ('position', )

    def __str__(self):
        return self.name