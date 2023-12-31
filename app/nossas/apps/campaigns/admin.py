from django.contrib import admin
from django.urls import path
from django.http.response import HttpResponseRedirect

from contrib.bonde.models import Mobilization, MobilizationStatus
from nossas.apps.baseadmin import OnSiteAdmin

from .models import Campaign, CampaignStatus


class CampaignAdmin(OnSiteAdmin):
    list_display = ("name", "status")
    change_list_template = "admin/campaigns/changelist.html"

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path("import/", self.import_mobilization),
        ]

        return my_urls + urls

    def import_mobilization(self, request):
        if request.method == "POST":
            mobilization_id = request.POST.get("mobilization_id")
            if mobilization_id:
                mobilization = Mobilization.objects.get(id=mobilization_id)

                Campaign.on_site.create(
                    name=mobilization.name,
                    description_pt_br=mobilization.goal,
                    status=CampaignStatus.closed
                    if mobilization.status != MobilizationStatus.active
                    else CampaignStatus.opened,
                    site=request.current_site
                )

                self.message_user(request, "Campanha importada com sucesso", "SUCCESS")

        return HttpResponseRedirect("../")


admin.site.register(Campaign, CampaignAdmin)
