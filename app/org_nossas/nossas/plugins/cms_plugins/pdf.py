from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.pdfmodel import PDFViewer


@plugin_pool.register_plugin
class PdfViewerPlugin(CMSPluginBase):
    name = "PDF Viewer"
    module = "NOSSAS"
    model = PDFViewer
    render_template = "nossas/plugins/pdf.html"