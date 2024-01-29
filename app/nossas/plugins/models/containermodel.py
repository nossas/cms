from nossas.design.models import (
    UICMSPlugin,
    UIBackgroundMixin,
    UIPaddingMixin,
    UIBorderMixin,
    NamingPluginMixin,
)


class Container(
    UIBackgroundMixin, UIPaddingMixin, UIBorderMixin, NamingPluginMixin, UICMSPlugin
):
    pass
