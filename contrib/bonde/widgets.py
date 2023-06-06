from django.forms import MultiWidget, Select


class BondeWidget(MultiWidget):
    description = "A Bonde widget reference"
    template_name = "bonde/widgets/bonde_widget.html"

    def __init__(self, *args, **kwargs):
        kwargs["widgets"] = {
            "mobilization_id": Select,
            "widget_id": Select
        }

        super(BondeWidget, self).__init__(*args, **kwargs)
    

    def decompress(self, value):
        if value:
            return [value.mobilization_id, value.widget_id]
        return []