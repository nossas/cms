from django.contrib import admin

from ..forms.institutional import InstitutionalInformationForm
from ..models.institutional import InstitutionalInformation


class InstitutionalInformationAdmin(admin.ModelAdmin):
    form = InstitutionalInformationForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "address_line",
                    ("city", "state"),
                    "zipcode",
                ),
            },
        ),
        (
            "Contato",
            {
                "fields": (("contact_mail", "contact_phone"),),
            },
        ),
    )
    change_form_template = "admin/institutional/change_form.html"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.site = request.current_site

        return super().save_model(request, obj, form, change)


admin.site.register(InstitutionalInformation, InstitutionalInformationAdmin)
