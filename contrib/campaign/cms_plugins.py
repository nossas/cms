from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import ActionButton, Row, Column
from .forms import PressureForm


# @plugin_pool.register_plugin
# class BlockPlugin(CMSPluginBase):
#     model = Block
#     name = "Bloco"
#     render_template = "campaign/plugins/block.html"
#     allow_children = True
#     child_classes = [
#         "PicturePlugin",
#         "TextPlugin",
#         "ActionButtonPlugin",
#         "RowPlugin",
#     ]


# @plugin_pool.register_plugin
# class GridBlockPlugin(CMSPluginBase):
#     model = Block
#     name = "Grid"
#     render_template = "campaign/plugins/grid-block.html"
#     allow_children = True
#     child_classes = ["TextPlugin", "PressurePlugin"]


@plugin_pool.register_plugin
class ActionButtonPlugin(CMSPluginBase):
    model = ActionButton
    name = "Botão de ação"
    render_template = "campaign/plugins/action-button.html"
    allow_children = False


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    render_template = "campaign/plugins/pressure.html"

    def render(self, context, instance, placeholder):
        context = super(PressurePlugin, self).render(context, instance, placeholder)
        context.update({"form": PressureForm()})
        return context


@plugin_pool.register_plugin
class RowPlugin(CMSPluginBase):
    model = Row
    name = "Linha"
    render_template = "campaign/plugins/row.html"
    allow_children = True
    child_classes = ["ColumnPlugin", "PicturePlugin"]


# @plugin_pool.register_plugin
# class ColumnPlugin(CMSPluginBase):
#     model = Column
#     name = "Coluna"
#     render_template = "campaign/plugins/column.html"
#     allow_children = True
#     parent_classes = ["RowPlugin"]


@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    name = "Rodapé"
    render_template = "campaign/plugins/footer.html"
    allow_children = False
