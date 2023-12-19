from django.contrib.sites.models import Site
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from .models import ThemeScss


@receiver(post_save, sender=Site)
def create_theme_scss(sender, instance, **kwargs):
    """This signal creates/updates a GA object 
    after creating/updating a Site object.
    """
    obj, created = ThemeScss.objects.update_or_create(
        site=instance
    )

    if not created:
        obj.save()