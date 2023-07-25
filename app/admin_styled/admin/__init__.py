from django.contrib import admin
from cms.models.pagemodel import Page

from .cms import NewPageAdmin
from .sites import AdminStyledSite


admin.site.unregister(Page)
admin.site.register(Page, NewPageAdmin)


site = AdminStyledSite(name="adminstyled")
