from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Counter

@plugin_pool.register_plugin
class CounterPlugin(CMSPluginBase):
  name = "Counter"
  model = Counter
  render_template = "counter/plugins/counter.html"

  def render(self, context, instance, placeholder):
      return super().render(context, instance, placeholder)
