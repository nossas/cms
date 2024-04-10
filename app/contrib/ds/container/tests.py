from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase

from .cms_plugins import ContainerPlugin


# Create your tests here.
class ContainerPluginsTestCase(CMSTestCase):

    def setUp(self):
        self.language = "pt-br"
        self.home = create_page(
            title="home", template="ds/base.html", language=self.language
        )
        self.home.publish(self.language)
        self.placeholder = self.home.placeholders.get(slot="content")
        self.superuser = self.get_superuser()

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()
        # if self.file:
        #     self.file.delete()
        #     del self.file
        #     with self.assertRaises(AttributeError):
        #         print(self.file)
        # if self.folder:
        #     self.folder.delete()
        #     del self.folder
        #     with self.assertRaises(AttributeError):
        #         print(self.folder)

    def test_container_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ContainerPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "ContainerPlugin")

    def test_add_container_plugins_on_generic_module(self):
        self.assertEqual(ContainerPlugin.module, "Generic")

    def test_container_permitted_children(self):
        self.assertEqual(ContainerPlugin.allow_children, True)