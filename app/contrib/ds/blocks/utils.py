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
    """Generator child plugins by schema

    Schema Properties:

        - attrs?: dict with field values of root plugin
        - children?: array of schema type
        - plugin_type: required only childs schema
    """
    from cms.api import add_plugin

    attrs = schema.get("attrs", None)
    if attrs and len(attrs.keys()) > 0:
        for field_name in attrs.keys():
            if field_name == "attributes":
                obj.attributes.update(attrs[field_name])
            else:
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
