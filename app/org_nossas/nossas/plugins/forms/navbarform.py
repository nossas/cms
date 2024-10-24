from django import forms

from org_nossas.nossas.design.forms import UIBackgroundFormMixin

from org_nossas.nossas.plugins.models.navbarmodel import Navbar


class NavbarPluginForm(UIBackgroundFormMixin, forms.ModelForm):
    class Meta:
        model = Navbar
        entangled_fields = {"attributes": []}
