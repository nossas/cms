import json
from typing import Any, Optional
from django import forms


class RadioSelect(forms.RadioSelect):
    template_name = "tailwind/widgets/radio.html"
    option_template_name = "tailwind/widgets/radio_option.html"


class InputArrayWidget(forms.MultiWidget):
    template_name = "tailwind/widgets/input_array.html"

    def get_context(self, name, value, attrs):
        if type(value) == str:
            value = json.loads(value)
        
        value = list(filter(lambda x: x, value))

        return {
            "widget": {"name": name, "value": value, "attrs": attrs},
            "input_array_limit": len(self.widgets),
        }

    def decompress(self, value):
        return json.loads(value)