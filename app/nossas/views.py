from django.views.generic import TemplateView

class StyleGuideView(TemplateView):
    template_name = "styleguide.html"
    name = "StyleGuide Nossas"
