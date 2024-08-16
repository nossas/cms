from django import forms

from cms.test_utils.testcases import CMSTestCase

from ..fields import InlineArrayWidget, InlineArrayField


# Create your tests here.
class InlineArrayTestCase(CMSTestCase):
    def test_inline_array_widget_render(self):
        widget = InlineArrayWidget(widget=forms.URLInput, size=3)
        name = 'social_media'
        value = ["http://nosssas.com", "http://nosssas.org", "http://nosssas.net"]
        html = widget.render(name, value)
        
        self.assertIn('http://nosssas.com', html)
        self.assertIn('http://nosssas.org', html)
        self.assertIn('http://nosssas.net', html)

    def test_inline_array_field_clean(self):
        field = InlineArrayField(forms.URLField(), size=3, required=False)
        value = ["http://nossas.com", "http://nossas.org", "http://nossas.net"]
        cleaned_value = field.clean(value)
        self.assertEqual(cleaned_value, value)
