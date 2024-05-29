from cms.plugin_pool import plugin_pool

from djangocms_picture.cms_plugins import PicturePlugin as DjangoCMSPicturePlugin

from django.conf import settings


plugin_pool.unregister_plugin(DjangoCMSPicturePlugin)


@plugin_pool.register_plugin
class PicturePlugin(DjangoCMSPicturePlugin):
    def render(self, context, instance, placeholder):
        use_responsive_img = False
        if instance.use_responsive_image == 'inherit':
            use_responsive_img = settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES
        elif instance.use_responsive_image == 'yes':
            use_responsive_img = True
        
        if use_responsive_img:
            classes = 'img-fluid ' + instance.attributes.get('class', '')
            instance.attributes['class'] = classes

        return super().render(context, instance, placeholder)