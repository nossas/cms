from org_nossas.nossas.design.models import UICMSPlugin, UIBackgroundMixin


class Navbar(UIBackgroundMixin, UICMSPlugin):
    def get_classes(self):
        classes = super().get_classes()

        return ["sticky-top"] + classes
