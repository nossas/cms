from django.views.generic.detail import DetailView

from .models import Campaign


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = "nossas/campaigns/campaign_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "navbar": {"classes": "bg-verde-nossas"},
            }
        )

        return context