from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FormEntriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'form_entries'
    verbose_name = _('Forms')