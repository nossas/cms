# from unittest.mock import patch
import pytest
import mock
from unittest.mock import call

# from django.test.client import RequestFactory

from cms import api

# from cms.test_utils.testcases import CMSTestCase
# from cms.plugin_rendering import ContentRenderer

from ..models import Block, BlockLayout


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

    from ..utils import template_plugin_generator

    item = {"plugin_type": "TextPlugin", "attrs": {"body": "<p>test</p>"}}
    all(template_plugin_generator(obj=plugin, schema={"children": [item]}))

    spy.assert_called_once_with(
        placeholder=plugin.placeholder,
        plugin_type=item["plugin_type"],
        language=plugin.language,
        target=plugin,
        **item["attrs"],
    )


@pytest.mark.django_db
def test_utils_template_by_schema_with_children(mocker, plugin):
    spy = mocker.spy(api, "add_plugin")

    from ..utils import template_plugin_generator

    item1 = {"plugin_type": "TextPlugin", "attrs": {"body": "<h2>Test</h2><p>test</p>"}}
    item2 = {"plugin_type": "ButtonPlugin", "attrs": {}}

    all(template_plugin_generator(obj=plugin, schema={"children": [item1, item2]}))

    assert spy.mock_calls == [
        call(
            placeholder=plugin.placeholder,
            plugin_type=item1["plugin_type"],
            language=plugin.language,
            target=plugin,
            **item1["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2["plugin_type"],
            language=plugin.language,
            target=plugin,
            **item2["attrs"],
        ),
    ]


@pytest.mark.django_db
def test_utils_template_by_schema_with_complex_children(mocker, plugin):
    spy = mocker.spy(api, "add_plugin")

    from ..utils import template_plugin_generator

    item1 = {"plugin_type": "TextPlugin", "attrs": {"body": "<h2>Test</h2>"}}

    item2_child = {"plugin_type": "TextPlugin", "attrs": {"body": "<p>Lorem</p>"}}
    item2_1 = {
        "plugin_type": "ColumnPlugin",
        "attrs": {"span": "4"},
        "children": [item2_child],
    }

    item2_2 = {
        "plugin_type": "ColumnPlugin",
        "attrs": {"span": "4"},
        "children": [item2_child],
    }

    item2_3 = {
        "plugin_type": "ColumnPlugin",
        "attrs": {"span": "4"},
        "children": [item2_child],
    }

    item2 = {
        "plugin_type": "BlockPlugin",
        "attrs": {"layout": "grid"},
        "children": [item2_1, item2_2, item2_3],
    }

    plugins = [
        p
        for p in template_plugin_generator(
            obj=plugin, schema={"children": [item1, item2]}
        )
    ]
    block_plugin = plugins[1]
    col_1_plugin = plugins[2]
    col_2_plugin = plugins[4]
    col_3_plugin = plugins[6]

    assert spy.mock_calls == [
        call(
            placeholder=plugin.placeholder,
            plugin_type=item1["plugin_type"],
            language=plugin.language,
            target=plugin,
            **item1["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2["plugin_type"],
            language=plugin.language,
            target=plugin,
            **item2["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2_1["plugin_type"],
            language=plugin.language,
            target=block_plugin,
            **item2_1["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2_child["plugin_type"],
            language=plugin.language,
            target=col_1_plugin,
            **item2_child["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2_2["plugin_type"],
            language=plugin.language,
            target=block_plugin,
            **item2_2["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2_child["plugin_type"],
            language=plugin.language,
            target=col_2_plugin,
            **item2_child["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2_3["plugin_type"],
            language=plugin.language,
            target=block_plugin,
            **item2_3["attrs"],
        ),
        call(
            placeholder=plugin.placeholder,
            plugin_type=item2_child["plugin_type"],
            language=plugin.language,
            target=col_3_plugin,
            **item2_child["attrs"],
        ),
    ]


@pytest.mark.django_db
@mock.patch.object(Block, "save")
def test_utils_template_update_objects(block_save_mock, plugin):
    from ..utils import template_plugin_generator

    all(
        template_plugin_generator(
            obj=plugin, schema={"attrs": {"layout": BlockLayout.flex}}
        )
    )

    assert block_save_mock.called == True


@pytest.mark.django_db
def test_utils_template_keep_attributes_when_update_object(plugin):
    from ..utils import template_plugin_generator

    plugin.attributes = {"background_color": "#c7c7c7"}
    plugin.save()

    all(
        template_plugin_generator(
            obj=plugin,
            schema={
                "attrs": {
                    "layout": BlockLayout.flex,
                    "attributes": {"alignment": "center"},
                }
            },
        )
    )

    assert plugin.attributes == {"background_color": "#c7c7c7", "alignment": "center"}
