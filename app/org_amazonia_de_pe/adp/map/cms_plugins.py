from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext as _
from .models import MapPlugin
from .forms import MapPluginForm

@plugin_pool.register_plugin
class MapPluginPublisher(CMSPluginBase):
    model = MapPlugin
    name = _("Mapa")
    render_template = "map/map.html"
    form = MapPluginForm
