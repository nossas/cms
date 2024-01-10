from nossas.design.models import (
    UICMSPlugin,
    UIBackgroundMixin,
    UIPaddingMixin,
    UIBorderMixin,
)


class Box(
    UIBackgroundMixin,
    UIPaddingMixin,
    UIBorderMixin,
    UICMSPlugin,
):
    pass
