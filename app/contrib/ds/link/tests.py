from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

# from .cms_plugins import GridPlugin, ColumnPlugin
from .models import Context, Target, Styled, Size, IconPosition


# Create your tests here.
class LinkPluginsTestCase(CMSTestCase):

    def setUp(self):
        self.language = "pt-br"
        self.home = create_page(
            title="home", template="ds/base.html", language=self.language
        )
        self.home.is_home = True
        self.home.save()
        
        self.home.publish(self.language)
        self.placeholder = self.home.placeholders.get(slot="content")
        self.superuser = self.get_superuser()

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()

    def test_button_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "ButtonPlugin")

    def test_button_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = "<a class='btn btn-primary' target='_self'>Enviar</a>"

        self.assertHTMLEqual(html, expected_html)

    def test_button_context_color_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            context=Context.success,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = "<a class='btn btn-success' target='_self'>Enviar</a>"

        self.assertHTMLEqual(html, expected_html)

    def test_button_target_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            link_target=Target._blank,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = "<a class='btn btn-primary' target='_blank'>Enviar</a>"

        self.assertHTMLEqual(html, expected_html)

    def test_button_external_link_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            external_link="https://nossas.org",
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = "<a class='btn btn-primary' href='https://nossas.org' target='_self'>Enviar</a>"

        self.assertHTMLEqual(html, expected_html)

    def test_button_internal_link_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            external_link="https://nossas.org",
            internal_link=self.home,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-primary' href='{self.home.get_absolute_url()}' target='_self'>Enviar</a>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_button_styled_outline(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            styled=Styled.outline
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-outline-primary' target='_self'>Enviar</a>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_button_context_styled_outline(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            context=Context.secondary,
            styled=Styled.outline
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-outline-secondary' target='_self'>Enviar</a>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_button_styled_inverted(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            styled=Styled.inverted
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-inverted-primary' target='_self'>Enviar</a>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_button_context_styled_inverted(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            context=Context.secondary,
            styled=Styled.inverted
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-inverted-secondary' target='_self'>Enviar</a>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_button_change_size(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            size=Size.small
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-primary btn-sm' target='_self'>Enviar</a>"
        )

        self.assertHTMLEqual(html, expected_html)
    
    def test_render_icon_button(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            icon="map-fill"
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-primary' target='_self'><i class='bi bi-map-fill'></i> Enviar</a>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_render_icon_button_position(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            icon="map-fill",
            icon_position=IconPosition.right
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-primary' target='_self'>Enviar <i class='bi bi-map-fill'></i></a>"
        )

        self.assertHTMLEqual(html, expected_html)

    def test_render_only_icon_button(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            icon="map-fill",
            icon_position=IconPosition.only
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<a class='btn btn-primary' target='_self' title='Enviar'><i class='bi bi-map-fill'></i></a>"
        )

        self.assertHTMLEqual(html, expected_html)
    
    def test_render_submit_button(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="ButtonPlugin",
            language=self.language,
            label="Enviar",
            link_target=Target.submit
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = (
            f"<button class='btn btn-primary' type='submit'>Enviar</button>"
        )

        self.assertHTMLEqual(html, expected_html)


# <i class="bi bi-map-fill"></i>