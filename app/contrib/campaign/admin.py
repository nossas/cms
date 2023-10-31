from django.contrib import admin
from cms.extensions import PageExtensionAdmin
from cms.models import Page
from cms.admin.pageadmin import PageAdmin

from cms.admin.forms import ChangePageForm

from .models import IconExtension, MetaDataExtension


class IconExtensionAdmin(PageExtensionAdmin):
    pass


class SimpleChangePageForm(ChangePageForm):
    meta_description = None


class SimplePageAdmin(PageAdmin):
    change_form = SimpleChangePageForm


admin.site.register(IconExtension, IconExtensionAdmin)
admin.site.register(MetaDataExtension, PageExtensionAdmin)

admin.site.unregister(Page)
admin.site.register(Page, SimplePageAdmin)