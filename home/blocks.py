from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from .forms import PressureForm, LoggedPressureForm


class TargetStructBlock(blocks.StructBlock):
    email_address = blocks.CharBlock()
    name = blocks.CharBlock()

    class Meta:
        icon = 'mail'
        template = 'home/blocks/target.html'


class PressureStructBlock(blocks.StructBlock):
    targets = blocks.StreamBlock([
        ('target', TargetStructBlock())
    ])
    subject = blocks.CharBlock()
    content = blocks.TextBlock()

    story = blocks.RichTextBlock()

    class Meta:
        icon = 'mail'
        template = 'home/blocks/pressure.html'
    

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        request = context['request']

        if request.user.is_authenticated:
            context['form'] = LoggedPressureForm(initial=dict(
                person_id=request.user.id,
                email_subject=value['subject'],
                email_body=value['content']
            ))

        else:
            context['form'] = PressureForm(initial=dict(
                email_subject=value['subject'],
                email_body=value['content']
            ))

        # import ipdb;ipdb.set_trace()
        return context


class HeroStructBlock(blocks.StructBlock):
    background = blocks.CharBlock(required=False)
    
    button = blocks.CharBlock(required=False)

    content = blocks.StreamBlock([
        ('heading', blocks.CharBlock(form_classname="h1")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock())
    ])

    class Meta:
        template = 'home/blocks/hero.html'


class SignatureStructBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock(required=False)

    partners = blocks.StreamBlock([
        ('partner', blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('external_url', blocks.URLBlock(required=False)),
            ('image', ImageChooserBlock())
        ]))
    ], required=False)

    class Meta:
        template = 'home/blocks/signature.html'