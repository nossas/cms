from nossas.design.models import (
    UIBackgroundMixin,
    UIBorderMixin,
    UIPaddingMixin,
    UICMSPlugin
)


class Box(
    UIBackgroundMixin,
    UIBorderMixin,
    UIPaddingMixin,
    UICMSPlugin
):
    pass
