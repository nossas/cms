from typing import Any
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from nossas.apps.baseadmin import OnSiteAdmin

from ..models.teams import MemberGroup, Member


class MemberAdmin(OnSiteAdmin):
    list_display = ("full_name", "member_group", "get_picture")

    def get_picture(self, obj):
        if obj.picture:
            return mark_safe(
                f"""<img src="{obj.picture.url}" height="50" width="50" />"""
            )

        return "-"

    get_picture.short_description = _("Imagem")


admin.site.register(MemberGroup, OnSiteAdmin)
admin.site.register(Member, MemberAdmin)
