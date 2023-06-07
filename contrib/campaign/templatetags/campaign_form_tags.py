from django import template


register = template.Library()


@register.filter
def add_class(field, class_name):
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })


@register.filter
def get_dict_value(data, key):
    if key in data:
        return data[key]
    else:
        return []