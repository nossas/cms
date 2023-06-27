import json
from django import forms
from django.core.exceptions import ValidationError

from .widgets import InputArrayWidget


class InputArrayField(forms.MultiValueField):
    def __init__(self, num_widgets=3, *args, **kwargs):
        list_fields = []
        list_widgets = []
        for i in range(0, num_widgets):
            list_fields.append(forms.CharField())
            list_widgets.append(forms.TextInput())

        self.widget = InputArrayWidget(widgets=list_widgets)

        super(InputArrayField, self).__init__(fields=list_fields, *args, **kwargs)

    def compress(self, data_list):
        return json.dumps(data_list)

    def clean(self, value):
        clean_data = list(filter(lambda x: x, value))

        if self.required and len(clean_data) == 0:
            raise ValidationError(self.error_messages['required'], code='required')

        out = self.compress(clean_data)
        self.validate(out)
        self.run_validators(out)
        return out