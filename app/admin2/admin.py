from django.contrib import admin


class ModelAdmin(admin.ModelAdmin):
    change_list_template = "admin2/change_list.html"
    change_form_template = "admin2/change_form.html"