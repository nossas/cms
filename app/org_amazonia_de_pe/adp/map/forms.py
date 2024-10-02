from django import forms
from .models import MapPlugin

class MapPluginForm(forms.ModelForm):
    class Meta:
        model = MapPlugin
        fields = ['url', 'width', 'height']