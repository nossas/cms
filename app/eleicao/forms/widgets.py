from typing import Any, Dict
from django.forms.widgets import Widget
import json


class SocialMedia(Widget):
    template_name = "eleicao/widgets/social_media.html"

    class Media:
        js = ["js/widgets/social-media.js", ]

    def get_context(self, name: str, value: Any, attrs) -> Dict[str, Any]:
        ctx = super().get_context(name, value, attrs)
        ctx['widget']['value'] = json.loads(value)
        return ctx

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, return the value
        of this widget or None if it's not provided.
        """
        total = int(len([v for k, v in data.items() if name in k]) / 2)
        values = []

        for i in range(total):
            kind_name = f"{name}.{i}.kind"
            url_name = f"{name}.{i}.url"
            
            values.append(dict(kind=data.get(kind_name), url=data.get(url_name)))

        import ipdb;ipdb.set_trace()
        # return data.get(name)
        return json.dumps(values)