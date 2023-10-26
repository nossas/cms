from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import IconExtension, MetaDataExtension


class IconExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(IconExtension, IconExtensionAdmin)
admin.site.register(MetaDataExtension, PageExtensionAdmin)
