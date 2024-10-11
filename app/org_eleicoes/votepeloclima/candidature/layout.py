from crispy_forms.layout import Field


class NoCrispyField(Field):
    template = 'crispy/no_crispy_field.html'


class FileField(Field):
    template = 'crispy/file_field.html'