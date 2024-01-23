from nossas.design.models import UICMSPlugin, UIBackgroundMixin, UIPaddingMixin, UIBorderMixin


class Container(UIBackgroundMixin, UIPaddingMixin, UIBorderMixin, UICMSPlugin):
    pass
