from django import forms
from django.utils.translation import gettext_lazy as _

from cms.models.pagemodel import Page
from entangled.forms import EntangledModelFormMixin

from .models import Menu, MenuExtraLink

SPACING = [
    ("0.5", "1"),
    ("0.75", "2"),
    ("1", "3"),
    ("1.25", "4"),
    ("1.75", "5"),
    ("2", "6"),
    ("auto", "auto"),
]

class SpacingFormMixin(EntangledModelFormMixin):
    gap = forms.ChoiceField(choices=SPACING, required=False)
    gap_mobile = forms.ChoiceField(choices=SPACING, required=False)
    padding_top = forms.ChoiceField(choices=SPACING, required=False)
    padding_bottom = forms.ChoiceField(choices=SPACING, required=False)

    class Meta:
        entangled_fields = {
            "attributes": [
                "gap",
                "gap_mobile",
                "padding_top",
                "padding_bottom"
            ]
        }

class MenuForm(SpacingFormMixin, forms.ModelForm):
    class Meta:
        model = Menu
        entangled_fields = {
            "attributes": []
        }
        untangled_fields = [
            "color",
            "active_styled"
        ]

class MenuExtraLinkForm(forms.ModelForm):
    class Meta:
        model = MenuExtraLink
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_menu_pages = Page.objects.filter(in_navigation=True)
        self.fields['internal_link'].queryset = Page.objects.exclude(pk__in=default_menu_pages)
