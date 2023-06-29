# https://stackoverflow.com/questions/2821702/how-do-you-extend-the-site-model-in-django
from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def create_default_ga(sender, **kwargs):
    from django.contrib.sites.models import Site
    from contrib.ga.models import GA

    site = Site.objects.get(id=getattr(settings, 'SITE_ID', 1))

    if not GA.objects.exists():
        GA.objects.create(site=site)


class GaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contrib.ga'

    def ready(self):
        post_migrate.connect(create_default_ga, sender=self)

        from .signals import create_ga
