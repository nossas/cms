# from unittest.mock import patch
import pytest

# from django.test.client import RequestFactory

from cms import api

# from cms.test_utils.testcases import CMSTestCase
# from cms.plugin_rendering import ContentRenderer

# from ..cms_plugins import BlockPlugin


@pytest.fixture()
def plugin():
    # setUp
    language = "pt-br"
    home = api.create_page(title="home", template="ds/base.html", language=language)
    home.publish(language)
    placeholder = home.placeholders.get(slot="content")

    plugin = api.add_plugin(
        placeholder=placeholder, plugin_type="BlockPlugin", language=language
    )

    yield plugin

    # tearDown
    home.delete()


@pytest.mark.django_db
def test_utils_template_by_schema(mocker, plugin):
    spy = mocker.spy(api, "add_plugin")

    from ..utils import block_factory

    schema = [{"plugin_type": "TextPlugin", "attrs": {"body": "<p>test</p>"}}]
    block_factory(schema=schema, obj=plugin, placeholder=plugin.placeholder)

    spy.assert_called_once_with(
        placeholder=plugin.placeholder,
        plugin_type=schema[0]["plugin_type"],
        language=plugin.language,
        target=plugin,
        **schema[0]["attrs"],
    )


# obj: Block
"""
schema: [
    {
        plugin_type: str,
        data?: obj,
        children?: []
    }
]
"""
