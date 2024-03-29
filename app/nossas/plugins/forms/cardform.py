from django import forms
from django.utils.translation import gettext_lazy as _

# from cms.forms.fields import PageSelectFormField as PageSearchField
from cms.models import Page
from django_select2.forms import ModelSelect2Widget

from ..models.cardmodel import Card


class Select2PageSearchFieldMixin:
    search_fields = [
        'title_set__title__icontains',
        'title_set__menu_title__icontains',
        'title_set__slug__icontains'
    ]

    def label_from_instance(self, obj):
        return obj.get_title()


class Select2PageSelectWidget(Select2PageSearchFieldMixin, ModelSelect2Widget):
    site = None

    # show entries when clicking on it
    def build_attrs(self, base_attrs, extra_attrs=None):
        default_attrs = {"data-minimum-input-length": 0}
        default_attrs.update(base_attrs)
        attrs = super().build_attrs(default_attrs, extra_attrs=extra_attrs)
        return attrs

    def get_queryset(self):
        if self.site:
            return Page.objects.drafts().on_site(self.site)
        return Page.objects.drafts()

    # we need to implement jQuery ourselves, see #180
    class Media:
        js = (
            "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        )


class Select2PageSearchField(forms.ModelChoiceField):
    widget = Select2PageSelectWidget(attrs={"classes": "customizacao"})

    def __init__(self, *args, **kwargs):
        kwargs['queryset'] = self.widget.get_queryset()
        super().__init__(*args, **kwargs)


class CardPluginForm(forms.ModelForm):
    internal_link = Select2PageSearchField(
        label=_('Link interno'),
        required=False,
    )

    class Meta:
        model = Card
        fields = ["image", "tag", "internal_link", "external_link", "target"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from cms.models import Page
        self.fields['internal_link'].queryset = Page.objects.drafts().on_site()


class CreateCardPluginForm(CardPluginForm):
    title = forms.CharField(label=_("Título"))
    description = forms.CharField(label=_("Descrição"), widget=forms.Textarea, required=False)

    class Meta:
        model = Card
        fields = ["image", "tag", "title", "description", "internal_link", "external_link", "target"]
