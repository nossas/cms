from typing import Any, Callable, Optional, Sequence, Union
from django.contrib import admin
from django.http.request import HttpRequest

import admin2

from .forms import (
    ChangeGroupForm,
    MigrateGroupForm,
    ChangeCampaignForm,
    MigrateCampaignForm,
)
from .models import Group, Campaign, Action


class ActionAdmin(admin2.ModelAdmin):

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False


class GroupAdmin(admin2.ModelAdmin):
    form = MigrateGroupForm

    def get_form(
        self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any
    ) -> Any:
        if change:
            self.form = ChangeGroupForm
        else:
            self.form = MigrateGroupForm

        return super(GroupAdmin, self).get_form(request, obj, change, **kwargs)

    def get_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> Sequence[Callable[..., Any] | str]:
        if obj:
            return ["name", "reference_json"]

        return ["reference_json"]


class CampaignAdmin(admin2.ModelAdmin):
    form = MigrateCampaignForm
    prepopulated_fields = {"slug": ("name",)}

    def get_form(
        self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any
    ) -> Any:
        if change:
            self.form = ChangeCampaignForm
        else:
            self.form = MigrateCampaignForm

        return super(CampaignAdmin, self).get_form(request, obj, change, **kwargs)

    def get_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> Sequence[Callable[..., Any] | str]:
        if obj:
            return ["name", "slug", "settings", "owner_group"]

        return ["settings", "name", "slug", "owner_group"]


admin2.site.register(Action, ActionAdmin)

admin2.site.register(Group, GroupAdmin)

admin2.site.register(Campaign, CampaignAdmin)
