from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase
from cms.plugin_rendering import ContentRenderer

from .cms_plugins import BlockPlugin
from .models import BlockElement, BlockLayout


# Create your tests here.
class BlockPluginsTestCase(CMSTestCase):

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

    def test_block_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "BlockPlugin")

    def test_add_block_plugins_on_generic_module(self):
        self.assertEqual(BlockPlugin.module, "Generic")

    def test_block_permitted_and_render_children(self):
        self.assertEqual(BlockPlugin.allow_children, True)

    def test_default_block_plugin(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
        )
        model_instance.full_clean()

        self.assertEqual(model_instance.element, "div")
        self.assertEqual(model_instance.layout, "block")

    def test_default_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_section_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            element=BlockElement.section,
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<section></section>"

        self.assertHTMLEqual(html, expected_html)

    def test_container_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            is_container=True
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='container'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_container_size_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            is_container=True,
            attributes={"size": "fluid"},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='container-fluid'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_background_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            attributes={"background_color": "#c7c7c7"},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div style='background-color:#c7c7c7'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_background_container_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            is_container=True,
            attributes={"background_color": "#c7c7c7"},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = (
            "<div style='background-color:#c7c7c7'><div class='container'></div></div>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_padding_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            attributes={"padding": [{"side": "y", "spacing": "2"}]},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='py-2'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_grid_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.grid,
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='grid'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_grid_gap_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.grid,
            attributes={"gap": 1},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='grid' style='--bs-gap:1rem'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_grid_alignment_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.grid,
            attributes={"alignment": "center"},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='grid align-items-center'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_flex_default_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.flex
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='d-flex flex-column flex-md-row'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_flex_attrs_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.flex,
            attributes={
                "direction": "column",
                "wrap": "wrap"
            }
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='d-flex flex-wrap flex-column'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_flex_attrs_fill_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.flex,
            attributes={
                "fill": True
            }
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='d-flex d-flex-fill flex-column flex-md-row'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_flex_responsive_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.flex,
            attributes={
                "direction": "row"
            }
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='d-flex flex-column flex-md-row'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_flex_responsive_row_reverse_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.flex,
            attributes={
                "direction": "row-reverse"
            }
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='d-flex flex-column-reverse flex-md-row-reverse'></div>"

        self.assertHTMLEqual(html, expected_html)