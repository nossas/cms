from cms.admin.settingsadmin import SettingsAdmin
from cms.models.settingmodels import UserSettings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from cms.admin.pageadmin import PageAdmin
from cms.models.pagemodel import Page
from django.contrib.sites.models import Site
from cms.admin.pageadmin import BasePageAdmin

import admin2


class CustomPageAdmin(PageAdmin):
    change_list_template = "admin2/cms/page/tree/base.html"
    actions_menu_template = 'admin2/cms/page/tree/actions_dropdown.html'
    page_tree_row_template = 'admin2/cms/page/tree/menu.html'


admin2.site.register(UserSettings, SettingsAdmin)
admin2.site.register(User, UserAdmin)
admin2.site.register(Page, CustomPageAdmin)
admin2.site.register(Site)