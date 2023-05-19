from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import ActionButton, Block


@plugin_pool.register_plugin
class BlockPlugin(CMSPluginBase):
    model = Block
    name = "Bloco"
    render_template = "mob/plugins/block.html"
    allow_children = True
    child_classes = [
        "PicturePlugin",
        "TextPlugin",
        "ActionButtonPlugin"
    ]


@plugin_pool.register_plugin
class GridBlockPlugin(CMSPluginBase):
    model = Block
    name = "Grid"
    render_template = "mob/plugins/grid-block.html"
    allow_children = True
    child_classes = [
        "TextPlugin",
        "PressurePlugin"
    ]


@plugin_pool.register_plugin
class ActionButtonPlugin(CMSPluginBase):
    model = ActionButton
    name = "Botão de ação"
    render_template = "mob/plugins/action-button.html"
    allow_children = False



@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    render_template = "mob/plugins/pressure.html"