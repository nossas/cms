from typing import Any
from django.contrib import admin

import admin2

# from .models.plugins import PressurePluginModel
from .models.base import Pressure, EmailPressure, PhonePressure, TwitterPressure
from .models.targets import Target, Contact
from .forms.base import PressureAdminForm, PressureAdminChangeForm
from .forms.targets import TargetAdminForm


class ContactInline(admin.TabularInline):
    model = Contact


class TargetAdmin(admin2.ModelAdmin):
    form = TargetAdminForm
    inlines = (ContactInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.publish_on = request.current_site

        return super(TargetAdmin, self).save_model(request, obj, form, change)


admin2.site.register(Target, TargetAdmin)


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


class PressureAdmin(admin2.ModelAdmin):
    form = PressureAdminForm
    change_form_template = "pressure/admin/pressure_change_form.html"
    inlines = (EmailPressureInline, PhonePressureInline, TwitterPressureInline)

    class Media:
        js = ["pressure/js/tabs.js"]

    def get_form(self, request, obj, change=False, **kwargs: Any) -> Any:
        if change:
            self.form = PressureAdminChangeForm
        return super().get_form(request, obj, change, **kwargs)
    

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if change:
            obj.campaign = obj.campaign.id
        return super().save_model(request, obj, form, change)


admin2.site.register(Pressure, PressureAdmin)
