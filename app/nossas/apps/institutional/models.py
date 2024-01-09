from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext_lazy as _


class InstitutionalInformation(models.Model):
    address_line = models.CharField(_("Endereço"), max_length=255)
    city = models.CharField(_("Cidade"), max_length=100)
    state = models.CharField(_("UF"), max_length=2)
    zipcode = models.CharField(_("CEP"), max_length=7)
    contact_mail = models.EmailField(_("E-mail de contato"))
    contact_phone = models.CharField(_("Telefone de contato"), max_length=11)

    site = models.OneToOneField(Site, on_delete=models.CASCADE)

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("Informações Institucionais")
