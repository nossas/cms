from django import forms
from django.contrib import admin
from django.db import models
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .conf import settings
from .forms import FormBuilder, FormDefinitionAdminForm, FormFieldInlineForm
from .models import FormDefinition, FormField

class FormFieldInline(admin.StackedInline):
    model = FormField
    form = FormFieldInlineForm
    extra = 0

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(
                attrs={'rows': 4, 'cols': 50})
        },
    }

    def get_fieldsets(self, request, obj=None):
        fields = (
            ('label', 'field_type', 'required'),
            'initial', 'placeholder_text', 'help_text', 
            'choice_values', 'position', 
        )

        if settings.FORM_ENTRIES_ALLOW_CUSTOM_FIELD_NAME:
            fields = fields + ('field_name', )

        fieldsets = (
            (None, {
                'fields': fields
            }),
        )
        return fieldsets

    class Media:
        css = {
            'all': ('css/djangocms_forms/admin/djangocms_forms.css',)
        }
        js = (
            'js/djangocms_forms/libs/jquery.min.js',
            'js/djangocms_forms/libs/jquery-ui.min.js',

            'js/djangocms_forms/admin/jquery-inline-positioning.js',
            'js/djangocms_forms/admin/jquery-inline-rename.js',
            'js/djangocms_forms/admin/jquery-inline-collapsible.js',
            'js/djangocms_forms/admin/jquery-inline-toggle-fields.js',
        )


class FormPlugin(CMSPluginBase):
    name = settings.FORM_ENTRIES_PLUGIN_NAME
    module = settings.FORM_ENTRIES_PLUGIN_MODULE
    model = FormDefinition
    cache = False
    form = FormDefinitionAdminForm
    inlines = (FormFieldInline, )
    render_template = settings.FORM_ENTRIES_DEFAULT_TEMPLATE

    def get_fieldsets(self, request, obj=None):
        if settings.FORM_ENTRIES_FIELDSETS:
            return settings.FORM_ENTRIES_FIELDSETS

        fieldsets = (
            (None, {'fields': ('name', )}),

            (None, {
                'description': _('The <strong>Title</strong> and <strong>Description</strong> '
                                 'will display above the input fields and Submit button.'),
                'fields': ('title', 'description', )
            }),
        )
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        # returns the first template that exists, falling back to bundled template
        return select_template([
            instance.form_template,
            settings.FORM_ENTRIES_DEFAULT_TEMPLATE,
            'form_entries/templates/default.html'
        ])

    def render(self, context, instance, placeholder):
        context = super(FormPlugin, self).render(context, instance, placeholder)
        request = context['request']

        form = FormBuilder(
            initial={'referrer': request.path_info}, form_definition=instance,
            label_suffix='', auto_id='%s')

        # redirect_delay = instance.redirect_delay or \
        #     getattr(settings, 'FORM_ENTRIES_REDIRECT_DELAY', 1000)

        context.update({
            'form': form,
            'recaptcha_site_key': settings.FORM_ENTRIES_RECAPTCHA_PUBLIC_KEY,
            # 'redirect_delay': redirect_delay
        })
        return context


plugin_pool.register_plugin(FormPlugin)