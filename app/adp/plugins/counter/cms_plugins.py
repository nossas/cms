from datetime import date

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Counter

#TODO: Mudar cor a partir do tema do numero

@plugin_pool.register_plugin
class CounterPlugin(CMSPluginBase):
  name = "Counter"
  model = Counter
  render_template = "counter/plugins/counter.html"

  def render(self, context, instance, placeholder):
      context = super().render(context, instance, placeholder)

      context["counter_start_number"] = 0
      context["counter_end_number"] = instance.end_number

      if instance.start_date and instance.end_date:
          delta = instance.end_date - instance.start_date
          context["counter_end_number"] = delta.days

          #todo: teste e pensar em numero entrada e saida (nomes)

          if instance.start_date > instance.end_date:
            context["counter_end_number"] = (date.today() - instance.start_date) * -1
            context["counter_start_number"] = delta.days * -1
      
      return context
