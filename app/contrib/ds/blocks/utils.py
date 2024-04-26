def to_padding_css(padding):
    """transform padding JSON schema to css classes"""
    css_classes = []

    for property in padding:
        if (
            property["side"] == "x"
            and property["spacing"] != "0"
            and property["spacing"] != "auto"
        ):
            css_classes.append(f"p{property['side']}-sm-{property['spacing']}")
            css_classes.append(f"p{property['side']}-{int(property['spacing']) - 1}")
        else:
            css_classes.append(f"p{property['side']}-{property['spacing']}")

    return css_classes


def template_plugin_generator(obj, schema):
    from cms.api import add_plugin

    attrs = schema.get("attrs", None)
    if attrs and len(attrs.keys()) > 0:
        for field_name in attrs.keys():
            setattr(obj, field_name, attrs[field_name])
        obj.save()

    children = schema.pop("children", [])

    for item_schema in children:
        plugin = add_plugin(
            placeholder=obj.placeholder,
            plugin_type=item_schema["plugin_type"],
            language=obj.language,
            target=obj,
            **item_schema.get("attrs", {}),
        )

        yield plugin

        if len(item_schema.get("children", [])) > 0:
            yield from template_plugin_generator(plugin, item_schema)


# def get_classes(self):
#         classes = super().get_classes()

#         if self.attributes:
#             padding = self.attributes.get("padding")
#             if padding and len(padding) > 0:
#                 classes += list(map(self.format_padding, padding))

#         return classes

#     def format_padding(self, property):
#         if (
#             property["side"] == "x"
#             and property["spacing"] != "0"
#             and property["spacing"] != "auto"
#         ):
#             return f"p{property['side']}-sm-{property['spacing']} p{property['side']}-{int(property['spacing']) - 1}"

#         return f"p{property['side']}-{property['spacing']}"
