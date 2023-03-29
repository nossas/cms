from .conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin

class Form(models.Model):
    name = models.CharField(_('Name'), max_length=255, db_index=True, editable=False)

    class Meta:
        verbose_name = _('form')
        verbose_name_plural = _('forms')
    
    def __str__(self):
        return self.name


class FormDefinition(CMSPlugin):
    name = models.CharField(_('Form Name'), max_length=255)

    title = models.CharField(_('Title'), max_length=150, blank=True)
    description = models.TextField(_('Description'), blank=True)

    form_template = models.CharField(
        _('Form Template'), max_length=150, blank=True,
        choices=settings.FORM_ENTRIES_TEMPLATES,
        default=settings.FORM_ENTRIES_DEFAULT_TEMPLATE
    )

    class Meta:
        verbose_name = _('form')
        verbose_name_plural = _('forms')


class FormField(models.Model):
    form = models.ForeignKey(FormDefinition, related_name='fields', on_delete=models.CASCADE)
    field_type = models.CharField(
        _('Field Type'), max_length=100,
        choices=settings.FORM_ENTRIES_FIELD_TYPES,
        default=settings.FORM_ENTRIES_DEFAULT_FIELD_TYPE)
    label = models.CharField(_('name'), max_length=255)
    field_name = models.CharField(_('Custom Field Name'), max_length=255, blank=True)
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
    position = models.PositiveIntegerField(_('Position'), blank=True, null=True)

    class Meta:
        verbose_name = _('field')
        verbose_name_plural = _('fields')
        ordering = ('position', )
    
    def build_field_attrs(self, extra_attrs=None):
        '''Helper function for building an attribute dictionary for form field.'''
        attrs = {}
        if extra_attrs:
            attrs.update(extra_attrs)

        attrs = {
            'required': self.required,
            'label': self.label if self.label else '',
            'initial': self.initial if self.initial else None,
            'help_text': self.help_text,
        }
        return attrs

    def build_widget_attrs(self, extra_attrs=None):
        '''Helper function for building an attribute dictionary for form widget.'''
        attrs = {}
        if extra_attrs:
            attrs.update(extra_attrs)

        if (self.required and settings.FORM_ENTRIES_USE_HTML5_REQUIRED
                and 'required' not in attrs and self.field_type not in ('hidden', 'radio', )):
            attrs['required'] = 'required'

        if self.field_type in settings.FORM_ENTRIES_FIELD_TYPES_WITH_PLACEHOLDER:
            if self.placeholder_text and not self.initial:
                attrs.update({
                    'placeholder': self.placeholder_text,
                })

        css_classes = {
            '__all__': (),
            'text': ('textinput',),
            'textarea': ('textarea', ),
            'email': ('emailinput', ),
            'number': ('integerfield', ),
            'phone': ('telephoneinput', ),
            'url': ('urlfield', ),
            'checkbox': ('booleanfield',),
            'checkbox_multiple': ('checkboxselectmultiple', ),
            'select': ('choicefield', ),
            'radio': ('radioselect', ),
            'file': ('filefield', ),
            'date': ('dateinput', ),
            'time': ('timeinput', ),
            'password': ('passwordinput', ),
            'hidden': ('hiddeninput', ),
        }

        css_classes.update(settings.FORM_ENTRIES_WIDGET_CSS_CLASSES)

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