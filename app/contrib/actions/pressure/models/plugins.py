from django.db import models

from cms.models import CMSPlugin

from contrib.bonde.models import Widget


class PressurePluginModel(CMSPlugin):
    """ """

    reference_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID de referência da widget na plataforma Bonde",
    )

    def get_widget(self):
        if not self.reference_id:
            return None

        return Widget.objects.get(id=self.reference_id)
