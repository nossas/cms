# https://stackoverflow.com/questions/2821702/how-do-you-extend-the-site-model-in-django
from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def create_default_themescss(sender, **kwargs):
    from django.contrib.sites.models import Site
    from contrib.designsystem.models import ThemeScss

    try:
        site = Site.objects.get(id=getattr(settings, "SITE_ID", 1))

        if not ThemeScss.objects.exists():
            ThemeScss.objects.create(site=site)
    except Site.DoesNotExist:
        pass


class DesignSystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contrib.designsystem"

    def ready(self):
        post_migrate.connect(create_default_themescss, sender=self)

        from .signals import create_theme_scss
