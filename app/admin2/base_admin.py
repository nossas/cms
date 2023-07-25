from django.contrib import admin


class ModelAdmin(admin.ModelAdmin):
    change_list_template = "admin2/change_list.html"
    change_form_template = "admin2/change_form.html"
    object_history_template = "admin2/object_history.html"
    delete_confirmation_template = "admin2/delete_confirmation.html"
    delete_selected_confirmation_template = "admin2/delete_selected_confirmation.html"