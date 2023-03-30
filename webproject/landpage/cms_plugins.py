from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Content


@plugin_pool.register_plugin
class ContentPlugin(CMSPluginBase):
    name = _('Content')
    module = _('Landpage')
    model = Content
    page_only = True
    allow_children = True
    render_template = 'landpage/content.html'