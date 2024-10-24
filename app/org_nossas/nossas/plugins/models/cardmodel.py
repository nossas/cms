from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from cms.models import CMSPlugin, Page
from filer.fields.file import FilerFileField

from org_nossas.nossas.design.models import NamingPluginMixin


TARGET_CHOICES = (
    ('_blank', _('Abrir em nova janela')),
    ('_self', _('Abrir na mesma janela')),
    # ('_parent', _('Delegate to parent')),
    # ('_top', _('Delegate to top')),
)

class AbstractLink(models.Model):
    # url_validators = [
    #     IntranetURLValidator(intranet_host_re=HOSTNAME),
    # ]

    # re: max_length, see: http://stackoverflow.com/questions/417142/
    external_link = models.CharField(
        verbose_name=_('Link externo'),
        blank=True,
        max_length=2040,
        # validators=url_validators,
        help_text=_('Forneça um link para uma fonte externa.'),
    )
    internal_link = models.ForeignKey(
        Page,
        verbose_name=_('Link interno'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Se fornecido, substitui o link externo.'),
    )

    # advanced options
    target = models.CharField(
        verbose_name=_('Target'),
        choices=TARGET_CHOICES,
        blank=True,
        max_length=255,
    )

    class Meta:
        abstract = True

    @property
    def link(self):
        pass

class Card(NamingPluginMixin, AbstractLink, CMSPlugin):
    image = FilerFileField(verbose_name=_("Imagem"), on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.CharField(verbose_name=_("Tag"), max_length=50, null=True, blank=True)

    def get_link(self):
        if self.internal_link:
            ref_page = self.internal_link
            link = ref_page.get_absolute_url()

            # simulate the call to the unauthorized CMSPlugin.page property
            cms_page = self.placeholder.page if self.placeholder_id else None

            # first, we check if the placeholder the plugin is attached to
            # has a page. Thus the check "is not None":
            if cms_page is not None:
                if getattr(cms_page, 'node', None):
                    cms_page_site_id = getattr(cms_page.node, 'site_id', None)
                else:
                    cms_page_site_id = getattr(cms_page, 'site_id', None)
            # a plugin might not be attached to a page and thus has no site
            # associated with it. This also applies to plugins inside
            # static placeholders
            else:
                cms_page_site_id = None

            # now we do the same for the reference page the plugin links to
            # in order to compare them later
            if cms_page is not None:
                if getattr(cms_page, 'node', None):
                    ref_page_site_id = ref_page.node.site_id
                else:
                    ref_page_site_id = ref_page.site_id
            # if no external reference is found the plugin links to the
            # current page
            else:
                ref_page_site_id = Site.objects.get_current().pk

            if ref_page_site_id != cms_page_site_id:
                ref_site = Site.objects._get_site_by_id(ref_page_site_id).domain
                link = f'//{ref_site}{link}'

        elif self.external_link:
            link = self.external_link

        else:
            link = None
        
        return link
            