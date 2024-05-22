from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase
from cms.plugin_rendering import ContentRenderer

from ..cms_plugins import BlockPlugin
from ..forms import BlockForm, BlockTemplateForm
from ..models import BlockElement, BlockLayout, FlexDirection
from contrib.ds.tests.helpers import get_filer_image


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

        self.image = get_filer_image()
        self.background_size = "cover"

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()

        if self.image:
            self.image.delete()
            del self.image
            with self.assertRaises(AttributeError):
                print(self.image)

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
            is_container=True,
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
            attributes={"padding_top": "2", "padding_bottom": "2"},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = "<div class='pt-2 pb-2'></div>"

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
            layout=BlockLayout.flex,
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
            attributes={"direction": "column", "wrap": "wrap"},
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
            attributes={"fill": True},
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
            attributes={"direction": "row"},
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
            attributes={"direction": "row-reverse"},
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = (
            "<div class='d-flex flex-column-reverse flex-md-row-reverse'></div>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_change_form_to_block_create_block(self):
        target = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
        )

        obj = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            target=target,
        )

        request = RequestFactory()
        get_request = request.get(
            "/admin/cms/page/add-plugin/?placeholder_id=3&plugin_type=BlockPlugin&cms_path=/&plugin_language=pt-br&plugin_parent=1"
        )

        instance, plugin = obj.get_plugin_instance()

        form = plugin.get_form(get_request, None, change=False, **{})

        self.assertEqual(form.__name__, BlockForm.__name__)

    def test_change_form_to_template_create_root_block(self):
        obj = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
        )

        request = RequestFactory()
        get_request = request.get(
            "/admin/cms/page/add-plugin/?placeholder_id=3&plugin_type=BlockPlugin&cms_path=/&plugin_language=pt-br"
        )

        instance, plugin = obj.get_plugin_instance()

        form = plugin.get_form(get_request, None, change=False, **{})

        self.assertEqual(form.__name__, BlockTemplateForm.__name__)

    def test_change_form_to_block_edit_root_block(self):
        obj = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
        )

        instance, plugin = obj.get_plugin_instance()

        form = plugin.get_form(None, obj, change=True, **{})

        self.assertEqual(form.__name__, BlockForm.__name__)

    def test_setup_initial_fields_on_template_block_form(self):
        form = BlockTemplateForm()

        self.assertEqual(form.fields["element"].initial, BlockElement.section)
        self.assertEqual(form.fields["is_container"].initial, True)
        self.assertEqual(form.fields["padding_top"].initial, "4")
        self.assertEqual(form.fields["padding_bottom"].initial, "4")

    def test_background_image_block_render_html(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            background_image=self.image,
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = f"""<div style="background-image:url('{self.image.url}');background-size:{self.background_size};background-repeat:no-repeat;background-position:center"></div>"""

        self.assertHTMLEqual(html, expected_html)

    def test_direction_change_mobile(self):
        model_instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type="BlockPlugin",
            language=self.language,
            layout=BlockLayout.flex,
            attributes={
                "direction": FlexDirection.column,
                "direction_mobile": FlexDirection.row,
            },
        )
        model_instance.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(model_instance, {})
        expected_html = f"""<div class="d-flex flex-md-column flex-row"></div>"""

        self.assertHTMLEqual(html, expected_html)
