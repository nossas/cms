from django.contrib import admin

# TODO: Mover esses imports para base de aplicativos e plugins
from nossas.apps.baseadmin import OnSiteAdmin

from .models import Publication
from .forms import PublicationForm


class PublicationAdmin(OnSiteAdmin):
    list_display = ("title", "slug", "parent", "created_at", "updated_at")
    form = PublicationForm
    prepopulated_fields = {'slug': ('title_pt_br',), }


admin.site.register(Publication, PublicationAdmin)
