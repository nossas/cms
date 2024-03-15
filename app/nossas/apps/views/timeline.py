from django.views.generic.detail import DetailView

from ..models.timeline import TimelineEvent


class TimelineDetailView(DetailView):
    model = TimelineEvent
    template_name = "nossas/timeline/detail.html"
    context_object_name = "event"
