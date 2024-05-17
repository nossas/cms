# Configuração do toolbar_CMS
# https://github.com/django-cms/djangocms-text-ckeditor/tree/master#ckeditor_settings

# Font Plugin
# Config: project.settings.ckeditor.font

config = {
    "toolbar_CMS": [
        # ['cmsplugins', 'cmswidget', '-', 'ShowBlocks'],
        ['cmsplugins'],
        [
            "Bold",
            "Italic",
            "Underline",
            "Strike",
            "-",
            "RemoveFormat",
        ],
        ["Link", "Unlink"],
        ["Format", "Font"],
        "/",
        [
            "FontSize",
            "-",
            "JustifyLeft",
            "JustifyCenter",
            "JustifyRight",
            "JustifyBlock",
        ],
        ["TextColor", "BGColor", "-", "PasteText", "PasteFromWord"],
        ["NumberedList", "BulletedList"],
        ["Undo", "Redo"],
    ]
}
