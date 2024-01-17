from django.contrib import admin

from django.urls import path
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from nossas.apps.baseadmin import OnSiteAdmin

from .models import Campaign
from .utils import import_mobilization


@admin.action(description=_("Mostrar todas as campanhas selecionadas"))
def show(modeladmin, request, queryset):
    queryset.update(hide=False)


class CampaignAdmin(OnSiteAdmin):
    list_display = ("name", "release_date", "status", "tag_list", "get_picture", "hide")
    change_list_template = "admin/campaigns/changelist.html"
    list_filter = ["hide", "campaign_group", "status", "tags"]
    search_fields = ["name", "status"]
    actions = [show]

    def tag_list(self, obj):
        return mark_safe(
            "<ul class='tags'>"
            + "".join(f"<li>{t.name}</li>" for t in obj.tags.all())
            + "</ul>"
        )

    tag_list.short_description = _("Marcadores")

    def get_picture(self, obj):
        if obj.picture:
            return mark_safe(
                f"""<img src="{obj.picture.url}" height="50" width="50" />"""
            )

        return "-"

    get_picture.short_description = _("Imagem")

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path("import/", self.import_mobilization),
        ]

        return my_urls + urls

    def import_mobilization(self, request):
        if request.method == "POST":
            mobilization_id = request.POST.get("mobilization_id")
            current_site = request.current_site
            current_user = request.user

            if mobilization_id:
                import_mobilization(mobilization_id, current_site, current_user)

                self.message_user(request, "Campanha importada com sucesso", "SUCCESS")

        return HttpResponseRedirect("../")


admin.site.register(Campaign, CampaignAdmin)
