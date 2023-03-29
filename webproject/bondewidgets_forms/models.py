import re

from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin

from .conf import settings

class Form(models.Model):
    
    name = models.CharField(_('Form Name'), max_length=255)

    def __str__(self):
        return self.name


class FormDefinition(CMSPlugin):
    """
    Form represents Bonde Form
    """
    title = models.CharField(_('Title'), max_length=150, blank=True)
    description = models.TextField(_('Description'), blank=True)

    # Reference model to relationship fields and definitions plugin
    form = models.ForeignKey(Form, related_name='definition', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('form')
        verbose_name_plural = _('forms')
    
    def __str__(self):
        return f'({self.title})'


class FormField(CMSPlugin):
    """
    Form Field represents Bonde Form
    """
    field_type = models.CharField(
        _('Field Type'), max_length=100,
        choices=settings.BONDEWIDGETS_FORMS_FIELD_TYPES,
        default=settings.BONDEWIDGETS_FORMS_DEFAULT_FIELD_TYPE)
    label = models.CharField(_('name'), max_length=255)
    field_name = models.CharField(_('Custom Field Name'), max_length=255)
    placeholder_text = models.CharField(_('Placeholder Text'), blank=True, max_length=100)
    required = models.BooleanField(_('Required'), default=True)
    help_text = models.TextField(
        _('Description'), blank=True,
        help_text=_('A description / instructions for this field.'))
    initial = models.CharField(_('Default Value'), max_length=255, blank=True)
    choice_values = models.TextField(
        _('Choices'),  blank=True,
        help_text=_('Enter options one per line. For "File Upload" '
                    'field type, enter allowed filetype (e.g .pdf) one per line.'))

    # Reference model to relationship fields and definitions plugin
    form = models.ForeignKey(Form, related_name='fields', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('field')
        verbose_name_plural = _('fields')
        ordering = ('position', )

    def __str__(self):
        return f'({self.field_name})'

    def build_field_attrs(self, extra_attrs=None):
        '''Helper function for building an attribute dictionary for form field.'''
        attrs = {}
        if extra_attrs:
            attrs.update(extra_attrs)

        attrs = {
            'required': self.required,
            'label': self.label if self.label else '',
            'initial': self.initial if self.initial else None,
            'help_text': self.help_text
        }

        return dict((k, v) for k,v in attrs.items() if v is not None)

    def build_widget_attrs(self, extra_attrs=None):
        '''Helper function for building an attribute dictionary for form widget.'''
        attrs = {}
        if extra_attrs:
            attrs.update(extra_attrs)
        
        if (self.required and settings.BONDEWIDGETS_FORMS_USE_HTML5_REQUIRED
                and 'required' not in attrs and self.field_type not in ('hidden', 'radio', )):
            attrs['required'] = 'required'

        if self.field_type in settings.BONDEWIDGETS_FORMS_FIELD_TYPES_WITH_PLACEHOLDER:
            if self.placeholder_text and not self.initial:
                attrs.update({
                    'placeholder': self.placeholder_text,
                })

        css_classes = {
            '__all__': ('form-control', ),
        }

        css_classes = (attrs.get('class', ''), ) + \
            css_classes.get('__all__', ()) + \
            css_classes.get(self.field_type, ())

        attrs['class'] = ' '.join(cls.strip() for cls in css_classes if cls.strip())

        return attrs
    
    def get_choices(self):
        if self.choice_values:
            regex = re.compile('[\s]*\n[\s]*')
            choices = regex.split(self.choice_values)
            return [(choice, choice) for choice in choices]