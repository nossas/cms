from crispy_forms.layout import Field


class NoCrispyField(Field):
    template = 'crispy/no_crispy_field.html'
