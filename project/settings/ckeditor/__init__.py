from .font import config as font_config
from .toolbar import config as toolbar_config

# CKEditor
# https://github.com/django-cms/djangocms-text-ckeditor#configuration

CKEDITOR_SETTINGS = {
    # "stylesSet": "default:/static/js/addons/ckeditor.wysiwyg.js",
    **font_config,
    **toolbar_config,
}

TEXT_INLINE_EDITING = True