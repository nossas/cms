from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from cms.utils.urlutils import admin_reverse

from .models import InstitutionalInformation



# @admin.site.login_required
# def redirect_add_or_change(request):
#     # perform some custom action
#     # ...
#     url = admin_reverse("institutional_institutionalinformation_add")

#     if request.current_site.institutionalinformation:
#         url = admin_reverse(
#             "institutional_institutionalinformation_change",
#             kwargs={"object_id": request.current_site.institutionalinformation.id},
#         )

#     return redirect(url)

# # register the custom view
# admin.site.register_view('redirect-add-or-change/', view=redirect_add_or_change, name='institutional_redirect_add_or_change')


class InstitutionalInformationAdmin(admin.ModelAdmin):
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

    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('^redirectaddorchange/$', self.redirect_add_or_change, name="redirectaddorchange"),
    #     ]
    #     return my_urls + urls

    # def redirect_add_or_change(self, request, **kwargs):
    #     # perform some custom action
    #     # ...
    #     url = admin_reverse("institutional_institutionalinformation_add")

    #     if request.current_site.institutionalinformation:
    #         url = admin_reverse(
    #             "institutional_institutionalinformation_change",
    #             kwargs={"object_id": request.current_site.institutionalinformation.id},
    #         )
        
    #     return redirect(url)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.site = request.current_site

        return super().save_model(request, obj, form, change)


admin.site.register(InstitutionalInformation, InstitutionalInformationAdmin)
