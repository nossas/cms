from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from cms.cms_toolbars import PAGE_MENU_ADD_IDENTIFIER


# class MobToolbarClass(CMSToolbar):
    
    # def populate(self):
        # import ipdb;ipdb.set_trace()

        # self.toolbar.get_or_create_menu(
        #     'mob_cms_integration-mob',  # a unique key for this menu
        #     'Mob',                      # the text that should appear in the menu
        #     )
        # import ipdb;ipdb.set_trace()
        # menu = self.get_menu(PAGE_MENU_ADD_IDENTIFIER)

        # self.toolbar.add_menu
        # self.toolbar.add_modal_button("Criar campanha", "/mob_wizard/create/", side=self.toolbar.RIGHT)
    
    # def post_template_populate(self):
    #     super(MobToolbarClass, self).post_template_populate()

    #     self.toolbar.add_modal_button("Criar campanha", "/mob_wizard/create/", side=self.toolbar.RIGHT)
            

# toolbar_pool.register(MobToolbarClass)




# @toolbar_pool.register
# class PlaceholderToolbar(CMSToolbar):
#     """
#     Adds placeholder edit buttons if placeholders or static placeholders are detected in the template
#     """

#     def populate(self):
#         self.page = get_page_draft(self.request.current_page)

#     def post_template_populate(self):
#         super().post_template_populate()
#         self.add_wizard_button()

#     def add_wizard_button(self):
#         from cms.wizards.wizard_pool import entry_choices
#         title = _("Create")

#         if self.page:
#             user = self.request.user
#             page_pk = self.page.pk
#             disabled = len(list(entry_choices(user, self.page))) == 0
#         else:
#             page_pk = ''
#             disabled = True

#         url = '{url}?page={page}&language={lang}&edit'.format(
#             url=reverse("cms_wizard_create"),
#             page=page_pk,
#             lang=self.toolbar.site_language,
#         )
#         self.toolbar.add_modal_button(title, url,
#                                       side=self.toolbar.RIGHT,
#                                       disabled=disabled,
#                                       on_close=REFRESH_PAGE)