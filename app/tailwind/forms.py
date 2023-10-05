from django import forms


class StyledBaseForm(forms.Form):
    """ """

    class Meta:
        readonly_fields = []
        input_classnames = [
            "block",
            "input",
            "input-bordered",
            "px-2.5",
            "pb-2.5",
            "pt-8",
            "w-full",
            "text-sm",
            "focus:outline-none",
            "focus:ring-0",
            "peer",
        ]

    def __init__(self, *args, **kwargs):
        super(StyledBaseForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            # Add custom class for fields
            visible.field.widget.attrs["class"] = " ".join(self.Meta.input_classnames)

            # Add custom class for textarea height
            if isinstance(visible.field.widget, forms.Textarea):
                visible.field.widget.attrs["class"] += " h-28"

            # Add readonly fields
            if visible.name in self.Meta.readonly_fields:
                visible.field.widget.attrs["disabled"] = True
                visible.field.widget.attrs["readonly"] = True

            # Add placeholder to use focus animation label
            visible.field.widget.attrs["placeholder"] = " "
