from django import forms
from cms.models.pagemodel import Page
from .models import MenuExtraLink

class MenuExtraLinkForm(forms.ModelForm):
    class Meta:
        model = MenuExtraLink
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_menu_pages = Page.objects.filter(in_navigation=True)
        self.fields['internal_link'].queryset = Page.objects.exclude(pk__in=default_menu_pages)
