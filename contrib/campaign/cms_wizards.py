from django import forms


from cms.forms.wizards import CreateCMSPageForm
# from cms.admin.forms import AddPageForm
from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool
from cms.models import Page
from cms.utils.page_permissions import user_can_add_page, user_can_add_subpage

# from .forms.wizards import CreateCMSPageForm, CreateCMSSubPageForm
# from .wizards.wizard_base import Wizard
# from .wizards.wizard_pool import wizard_pool
from .forms import CreatePressureForm


class CMSPressureWizard(Wizard):

    def user_has_add_permission(self, user, page=None, **kwargs):
        if page:
            parent_page = page.get_parent_page()
        else:
            parent_page = None

        if page and page.get_parent_page():
            # User is adding a page which will be a right
            # sibling to the current page.
            has_perm = user_can_add_subpage(user, target=parent_page)
        else:
            has_perm = user_can_add_page(user)
        return has_perm


class CMSDonationWizard(Wizard):

    def user_has_add_permission(self, user, page=None, **kwargs):
        if page:
            parent_page = page.get_parent_page()
        else:
            parent_page = None

        if page and page.get_parent_page():
            # User is adding a page which will be a right
            # sibling to the current page.
            has_perm = user_can_add_subpage(user, target=parent_page)
        else:
            has_perm = user_can_add_page(user)
        return has_perm


cms_pressure_wizard = CMSPressureWizard(
    title="Campanha de Pressão",
    weight=100,
    form=CreatePressureForm,
    model=Page,
    description="Pressão por e-mail Explica tática"
)

cms_donation_wizard = CMSDonationWizard(
    title="Campanha de Doação",
    weight=100,
    form=CreatePressureForm,
    model=Page,
    description="Doação Explica tática"
)

wizard_pool.register(cms_pressure_wizard)
wizard_pool.register(cms_donation_wizard)