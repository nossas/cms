from django.contrib import admin

import urllib
from django.core.files import File as DjangoFile
from django.urls import path
from django.http.response import HttpResponseRedirect
from django.utils.safestring import mark_safe

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
    list_display = ("name", "release_date", "status", "tag_list", "get_picture", "hide")
    change_list_template = "admin/campaigns/changelist.html"
    list_filter = ["tags", "status", "hide"]
    search_fields = ["name", "status"]

    def tag_list(self, obj):
        return mark_safe(
            "<ul class='tags'>"
            + "".join(f"<li>{t.name}</li>" for t in obj.tags.all())
            + "</ul>"
        )

    tag_list.short_description = "Marcadores"

    def get_picture(self, obj):
        return mark_safe(f"""<img src="{obj.picture.url}" height="50" width="50" />""")

    get_picture.short_description = "Imagem"

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

                updated = False
                campaign = Campaign.on_site.create(
                    name=mobilization.name,
                    description_pt_br=mobilization.goal,
                    status=CampaignStatus.closed
                    if mobilization.status != MobilizationStatus.active
                    else CampaignStatus.opened,
                    site=request.current_site,
                )

                if mobilization.custom_domain:
                    updated = True
                    campaign.url = "https://" + mobilization.custom_domain

                if mobilization.theme:
                    updated = True
                    campaign.tags.add(mobilization.theme.label)

                if mobilization.subthemes.exists():
                    updated = True
                    campaign.tags.add(
                        *list(map(lambda x: x.label, mobilization.subthemes.all()))
                    )

                if mobilization.facebook_share_image:
                    updated = True
                    result = urllib.request.urlretrieve(
                        mobilization.facebook_share_image
                    )

                    image = create_filer_image(
                        request, f"mobilization_{mobilization.id}_image", result[0]
                    )

                    campaign.picture = image

                if mobilization.created_at:
                    updated = True
                    campaign.release_date = mobilization.created_at

                if updated:
                    campaign.save()

                self.message_user(request, "Campanha importada com sucesso", "SUCCESS")

        return HttpResponseRedirect("../")


admin.site.register(Campaign, CampaignAdmin)
