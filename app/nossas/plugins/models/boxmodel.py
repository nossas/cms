from nossas.design.models import (
    UICMSPlugin,
    UIBackgroundMixin,
    UIBorderMixin,
)


class Box(
    UIBackgroundMixin,
    UIBorderMixin,
    UICMSPlugin,
):
    pass
