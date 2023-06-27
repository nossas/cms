import json
from django import forms


class RadioSelect(forms.RadioSelect):
    template_name = "tailwind/widgets/radio.html"
    option_template_name = "tailwind/widgets/radio_option.html"


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'tailwind/widgets/checkbox_select.html'
    option_template_name = 'tailwind/widgets/checkbox_option.html'


class InputArrayWidget(forms.MultiWidget):
    template_name = "tailwind/widgets/input_array.html"

    class Media:
        js = ["js/input-array.js"]

    def get_context(self, name, value, attrs):
        if type(value) == str:
            value = json.loads(value)
        elif not value:
            value = []
        
        value = list(filter(lambda x: x, value))

        return {
            "widget": {
                "name": name,
                "value": value,
                "attrs": attrs,
                "media": self.media
            },
            "input_array_limit": len(self.widgets),
        }

    def decompress(self, value):
        return json.loads(value)