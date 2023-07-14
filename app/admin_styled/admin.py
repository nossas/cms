from django.contrib import admin
from cms.admin.forms import AddPageForm
from cms.admin.pageadmin import PageAdmin
from cms.models.pagemodel import Page

admin.site.unregister(Page)

class NewAddPageForm(AddPageForm):
    class Meta(AddPageForm.Meta):
        model = Page

    def __init__(self, *args, **kwargs):
        super(NewAddPageForm, self).__init__(*args, **kwargs)

        self.fields["source"].widget.choices = [
            (value, label.replace("---------", "Criar página do zero"))
            for value, label in self.fields["source"].widget.choices
        ]

class NewPageAdmin(PageAdmin):
    add_form = NewAddPageForm

admin.site.register(Page, NewPageAdmin)
