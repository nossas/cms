from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Content, Style

class InlineStyleAdmin(admin.StackedInline):
    model = Style


@plugin_pool.register_plugin
class ContentPlugin(CMSPluginBase):
    name = _('Content')
    module = _('Landpage')
    model = Content
    page_only = True
    allow_children = True
    render_template = 'landpage/content.html'
    inlines = (InlineStyleAdmin, )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context['styles'] = ';'.join(
            map(lambda style: f'{style.property}:{style.value}', instance.style_item.all()))

        return context