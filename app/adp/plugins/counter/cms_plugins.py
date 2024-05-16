from datetime import date

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Counter


@plugin_pool.register_plugin
class CounterPlugin(CMSPluginBase):
  name = "Counter"
  model = Counter
  render_template = "counter/plugins/counter.html"

  def render(self, context, instance, placeholder):
      context = super().render(context, instance, placeholder)

      context["counter_initial_number"] = 0
      context["counter_target_number"] = instance.target_number

      if instance.initial_date and instance.target_date:
          delta = instance.target_date - instance.initial_date
          context["counter_target_number"] = delta.days

          if instance.target_date > instance.initial_date:
              context["counter_target_number"] = (instance.target_date - date.today()).days
              context["counter_initial_number"] = (instance.target_date - instance.initial_date).days

      elif instance.target_date:
          delta = (date.today() - instance.target_date)
          context["counter_initial_number"] = 0
          context["counter_target_number"] = delta.days
      
      return context
