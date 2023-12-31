from django.contrib import admin

import urllib
from django.core.files import File as DjangoFile
from django.urls import path
from django.http.response import HttpResponseRedirect
from filer.models import Image

from contrib.bonde.models import Mobilization, MobilizationStatus
from nossas.apps.baseadmin import OnSiteAdmin

from .models import Campaign, CampaignStatus


def create_filer_image(request, filename, datafile):
    owner = request.user
    file_obj = DjangoFile(open(datafile, "rb"), name=filename)
    image = Image.objects.create(owner=owner, original_filename=filename, file=file_obj)
    return image


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

                campaign = Campaign.on_site.create(
                    name=mobilization.name,
                    description_pt_br=mobilization.goal,
                    status=CampaignStatus.closed
                    if mobilization.status != MobilizationStatus.active
                    else CampaignStatus.opened,
                    site=request.current_site,
                )

                if mobilization.facebook_share_image:
                    result = urllib.request.urlretrieve(
                        mobilization.facebook_share_image
                    )

                    image = create_filer_image(
                        request, f"mobilization_{mobilization.id}_image", result[0]
                    )

                    campaign.picture = image
                    campaign.save()

                self.message_user(request, "Campanha importada com sucesso", "SUCCESS")

        return HttpResponseRedirect("../")


admin.site.register(Campaign, CampaignAdmin)
