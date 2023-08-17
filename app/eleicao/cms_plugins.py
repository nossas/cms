# EleicaoNavbarPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class EleicaoNavbarPlugin(CMSPluginBase):
    name = "Navbar"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/navbar.html"


@plugin_pool.register_plugin
class EleicaoFooterPlugin(CMSPluginBase):
    name = "Assinatura"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/footer.html"