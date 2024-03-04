from typing import Any
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from adminsortable2.admin import SortableStackedInline, SortableAdminBase
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


class MemberStackedInline(SortableStackedInline):
    model = Member
    fields = ("my_order", )
    extra = 0

class MemberGroupAdmin(SortableAdminBase, OnSiteAdmin):
    list_display = ("name", "my_order")
    inlines = [MemberStackedInline]
    ordering = ("my_order", "id")


admin.site.register(MemberGroup, MemberGroupAdmin)
admin.site.register(Member, MemberAdmin)
