from typing import Any
from django.contrib import admin

from translated_fields import TranslatedFieldAdmin

from .models import MemberGroup, Member


class OnSiteAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    # model = MemberGroup

    def get_fields(self, request, obj):
        fields = super().get_fields(request, obj)
        fields.remove("site")
        return fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.site = request.current_site

        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = self.model.on_site.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
        # return super().get_queryset(request)


admin.site.register(MemberGroup, OnSiteAdmin)
admin.site.register(Member, OnSiteAdmin)
