from django import forms

from nossas.design.forms import UIBackgroundFormMixin

from nossas.plugins.models.navbarmodel import Navbar


class NavbarPluginForm(UIBackgroundFormMixin, forms.ModelForm):
    class Meta:
        model = Navbar
        entangled_fields = {"attributes": []}
