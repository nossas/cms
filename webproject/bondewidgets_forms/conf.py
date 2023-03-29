from django.conf import settings
from django.utils.translation import gettext_lazy as _

from appconf import AppConf


class BondeFormsConf(AppConf):
    FIELD_TYPES = (
        ('text', _('Text')),
        ('textarea', _('Text Area')),
        ('email', _('Email')),
        ('number', _('Number')),
        ('phone', _('Phone')),
        ('url', _('URL')),
        ('checkbox', _('Checkbox')),
        ('checkbox_multiple', _('Multi Checkbox')),
        ('select', _('Drop down')),
        ('radio', _('Radio')),
        ('file', _('File Upload')),
        ('date', _('Date')),
        ('time', _('Time')),
        ('password', _('Password')),
        ('hidden', _('Hidden')),
    )

    DEFAULT_FIELD_TYPE = 'text'

    FIELD_TYPES_WITH_PLACEHOLDER = (
        'text', 'textarea', 'email', 'number', 'phone', 'url', 'password',
    )

    USE_HTML5_REQUIRED = False

    HASHIDS_SALT = settings.SECRET_KEY

    class Meta:
        prefix = 'bondewidgets_forms'