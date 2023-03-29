import mock

from django.test import TestCase

from bondewidgets_forms.models import Form, FormField


class FormFieldTestCase(TestCase):

    def setUp(self):
        form = mock.Mock(spec=Form)
        form._state = mock.Mock()

        self.field = FormField()
        self.field.field_type = 'text'
        self.field.label = 'Name'
        self.field.field_name = 'name'
        self.field.placeholder_text = 'Whats your name?'
        self.field.required = True
        self.field.form = form

    def test_field_attrs(self):
        self.assertDictEqual(self.field.build_field_attrs(), {
            'required': self.field.required,
            'label': self.field.label,
            'help_text': ''
        })
    
    def test_widget_attrs(self):
        self.assertDictEqual(self.field.build_widget_attrs(), {
            'placeholder': self.field.placeholder_text,
            'class': 'form-control'
        })