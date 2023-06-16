from django.forms.widgets import ChoiceWidget


class SelectLayout(ChoiceWidget):
    template_name = 'frontend/landpage/forms/widgets/select_layout.html'

    # def get_context(self, name, value, attrs):
    #     return {
    #         'widget': {
    #             'name': name,
    #             'is_hidden': self.is_hidden,
    #             'required': self.is_required,
    #             'value': self.format_value(value),
    #             'attrs': self.build_attrs(self.attrs, attrs),
    #             'template_name': self.template_name,
    #         },
    #     }