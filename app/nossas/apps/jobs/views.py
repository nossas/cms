from django.db.models import Q
from django.views.generic import DetailView

from .models import Job, JobStatus


class JobDetailView(DetailView):
    model = Job
    template_name = "nossas/jobs/job_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = context["object"]
        context.update(
            {
                "navbar": {"classes": "bg-verde-nossas"},
                "job_list": Job.on_site.filter(~Q(id=object.pk)).filter(
                    ~Q(status=JobStatus.closed)
                ),
            }
        )

        return context
