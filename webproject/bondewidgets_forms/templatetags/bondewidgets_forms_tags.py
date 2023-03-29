from django import forms, template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def to_html(field):
    field_attrs = field.build_field_attrs()
    widget_attrs = field.build_widget_attrs()

    if field.field_type == 'text':
        field_attrs.update({
            'widget': forms.TextInput(attrs=widget_attrs)
        })

        return forms.CharField(**field_attrs)