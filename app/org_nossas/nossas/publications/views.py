from django.views.generic.detail import DetailView

from .models import Publication


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "nossas/publications/detail.html"