from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "logo")
