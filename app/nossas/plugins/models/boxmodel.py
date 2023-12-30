from nossas.design.models import (
    UIProperties,
    UIDefaultPropertiesMixin,
    UIBorderPropertiesMixin,
)


class Box(UIDefaultPropertiesMixin, UIBorderPropertiesMixin, UIProperties):
    pass
