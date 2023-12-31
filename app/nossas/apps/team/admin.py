from typing import Any
from django.contrib import admin

from nossas.apps.baseadmin import OnSiteAdmin

from .models import MemberGroup, Member


admin.site.register(MemberGroup, OnSiteAdmin)
admin.site.register(Member, OnSiteAdmin)
