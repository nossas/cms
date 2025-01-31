from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase

from ..cms_plugins import GridPlugin, ColumnPlugin


# Create your tests here.
class GridPluginsTestCase(CMSTestCase):

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

    def test_grid_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=GridPlugin.__name__,
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "GridPlugin")

    def test_column_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ColumnPlugin.__name__,
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "ColumnPlugin")

    def test_add_grid_plugins_on_generic_module(self):
        self.assertEqual(GridPlugin.module, "Generic")

    def test_add_column_plugin_only_grid(self):
        self.assertEqual(ColumnPlugin.parent_classes, [GridPlugin.__name__, "BlockPlugin"])

    # def test_add_columns_by_grid(self):
    #     plugin = add_plugin(
    #         placeholder=self.placeholder,
    #         plugin_type=GridPlugin.__name__,
    #         language=self.language,
    #         columns=2
    #     )
    #     plugin.full_clean()

    #     self.assertEqual(plugin.get)