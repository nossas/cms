from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin

# from autoslug import AutoSlugField

# Create your models here.
class Content(CMSPlugin):
    name = models.CharField(verbose_name=_('name'), max_length=30)
    slug = models.SlugField(max_length=40)
    is_menu = models.BooleanField(verbose_name=_('render menu'), default=True)
    
    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('contents')
        ordering = ('position', )

    def __str__(self):
        return self.name

    def copy_relations(self, old_instance):
        self.style_item.all().delete()

        for style_item in old_instance.style_item.all():
            style_item.pk = None
            style_item.plugin = self
            style_item.save()


class Style(models.Model):
    PROPERTIES = (
        ('background-color', _('Background Color')),
        ('background', _('Background')),
        ('background-size', _('Background Size'))
    )

    property = models.CharField(verbose_name=_('property'), max_length=30, choices=PROPERTIES)
    value = models.CharField(verbose_name=_('value'), max_length=150)

    plugin = models.ForeignKey(
        Content,
        related_name='style_item',
        on_delete=models.CASCADE
    )