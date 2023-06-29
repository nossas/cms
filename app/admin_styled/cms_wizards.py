from django.utils.translation import gettext_lazy as _

from cms.models import Page
from cms.wizards.wizard_pool import wizard_pool
from cms.forms.wizards import CreateCMSPageForm
from cms.cms_wizards import CMSPageWizard, cms_page_wizard

wizard_pool.unregister(cms_page_wizard)


class NewCreateCMSPageForm(CreateCMSPageForm):
    content = None

new_cms_page_wizard = CMSPageWizard(
    title=_("New page"),
    weight=100,
    form=NewCreateCMSPageForm,
    model=Page,
    description=_("Create a new page next to the current page.")
)

wizard_pool.register(new_cms_page_wizard)