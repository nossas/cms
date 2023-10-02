from django import forms
from django.conf import settings
from django.contrib.sites.models import Site

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Maps

@plugin_pool.register_plugin
class LeafletMapPlugin(CMSPluginBase):
    name = "Mapa"
    module = "Frontend"
    model = Maps
    render_template = "maps/plugins/map.html"

