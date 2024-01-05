from nossas.design.models import (
    UIProperties,
    UIDefaultPropertiesMixin,
    UIPaddingPropertiesMixin,
    UIBorderPropertiesMixin,
)


class Box(
    UIDefaultPropertiesMixin,
    UIPaddingPropertiesMixin,
    UIBorderPropertiesMixin,
    UIProperties,
):
    pass
