# from django import forms
# from django.db import models

from cms.models import Page
from django_select2.forms import ModelSelect2Widget
from org_nossas.nossas.design.fields import Select2PageSearchFieldMixin


class Select2CategorySelectWidget(Select2PageSearchFieldMixin, ModelSelect2Widget):
    site = None

    # show entries when clicking on it
    def build_attrs(self, base_attrs, extra_attrs=None):
        default_attrs = {"data-minimum-input-length": 0}
        default_attrs.update(base_attrs)
        attrs = super().build_attrs(default_attrs, extra_attrs=extra_attrs)
        return attrs

    def get_queryset(self):
        qs = Page.objects.drafts()
        if self.site:
            qs = Page.objects.drafts().on_site(self.site)

        return qs.filter(application_namespace__isnull=False).filter(
            application_namespace__icontains="publications"
        )

    # we need to implement jQuery ourselves, see #180
    class Media:
        js = ("https://code.jquery.com/jquery-3.5.1.slim.min.js",)
