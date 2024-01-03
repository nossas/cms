from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Job, JobStatus


@plugin_pool.register_plugin
class SliderJobsPlugin(CMSPluginBase):
    name = "Slide de Vagas"
    module = "NOSSAS"
    render_template = "plugins/slider_jobs_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update({"job_list": Job.on_site.filter(~Q(status=JobStatus.closed))})

        return context
