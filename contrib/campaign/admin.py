from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import Target, IconExtension


class IconExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(IconExtension, IconExtensionAdmin)

admin.site.register(Target)