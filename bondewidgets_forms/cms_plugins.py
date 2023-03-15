from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

# from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import FormBuilder, FieldForm
from .models import Form, FormDefinition, FormField


@plugin_pool.register_plugin
class FormPlugin(CMSPluginBase):
    name = _('Form')
    module = _('Bonde')
    model = FormDefinition
    # inlines = (FormAdmin, )
    allow_children = True
    child_classes = [
        'GridContainerPlugin',
        'GridRowPlugin',
        'FormFieldPlugin'
    ]
    render_template = 'bondewidgets/forms/form.html'

    def render(self, context, instance, placeholder):
        ctx = super(FormPlugin, self).render(context, instance, placeholder)
        path_info = ctx['request'].path_info
        is_draft = ctx['current_page'].publisher_is_draft

        form = FormBuilder(
            initial={'referrer': path_info},
            form_instance=instance.form,
            is_draft=is_draft,
            label_suffix='',
            auto_id='%s'
        )

        ctx.update({
            'form': form
        })

        return ctx

@plugin_pool.register_plugin
class FormFieldPlugin(CMSPluginBase):
    name = _('Field')
    module = _('Bonde')
    model = FormField
    # form = FieldForm
    require_parent = True
    parent_classes = [
        'GridColumnPlugin',
        'FormPlugin'
    ]
    render_template = 'bondewidgets/forms/field.html'
    
    def render(self, context, instance, placeholder):
        context = super(FormFieldPlugin, self).render(context, instance, placeholder)

        try:
            context.update({
                'field': context['form'][instance.field_name]
            })
        except KeyError:
            pass

        return context
