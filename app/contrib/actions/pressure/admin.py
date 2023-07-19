from typing import Any
from django.contrib import admin

from admin_styled.admin import site as admin_site

from .models.base import Pressure, EmailPressure, PhonePressure, TwitterPressure
from .models.targets import Target, Contact
from .forms.targets import TargetAdminForm


class ContactInline(admin.TabularInline):
    model = Contact


class TargetAdmin(admin.ModelAdmin):
    form = TargetAdminForm
    inlines = (ContactInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.publish_on = request.current_site

        return super(TargetAdmin, self).save_model(request, obj, form, change)


admin_site.register(Target, TargetAdmin)


class EmailPressureInline(admin.StackedInline):
    model = EmailPressure
    extra = 1
    max_num = 1
    template = "pressure/admin/pressure_inline_formset.html"


class PhonePressureInline(admin.StackedInline):
    model = PhonePressure
    extra = 1
    max_num = 1
    template = "pressure/admin/pressure_inline_formset.html"


class TwitterPressureInline(admin.StackedInline):
    model = TwitterPressure
    extra = 1
    max_num = 1
    template = "pressure/admin/pressure_inline_formset.html"


class PressureAdmin(admin.ModelAdmin):
    change_form_template = "pressure/admin/pressure_change_form.html"
    inlines = (EmailPressureInline, PhonePressureInline, TwitterPressureInline)

    class Media:
        # css = {
        #     "all": ["pressure/css/tabs.css"]
        # }
        js = ["pressure/js/tabs.js"]

    # def get_formsets_with_inlines(self, request, obj=None):
    #     for inline in self.get_inline_instances(request, obj):
    #         # hide MyInline in the add view
    #         # if not isinstance(inline, MyInline) or obj is not None:
    #         import ipdb;ipdb.set_trace()
    #         yield inline.get_formset(request, obj), inline


admin_site.register(Pressure, PressureAdmin)
