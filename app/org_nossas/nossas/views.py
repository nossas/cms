from django.views.generic import TemplateView
from .models import StyleGuideModel

class StyleGuideView(TemplateView):
    template_name = "styleguide.html"
    name = "StyleGuide Nossas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instances'] = StyleGuideModel.objects.all()
        return context
