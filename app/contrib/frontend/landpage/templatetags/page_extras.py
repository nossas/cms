from django import template

register = template.Library()


@register.inclusion_tag("frontend/landpage/plugins/footer.html")
def show_footer(styles=None, community_name=None, **kwargs):
    ctx = kwargs

    if styles:
        ctx.update({"instance": {"styles": styles}})

    if community_name:
        ctx.update({"community": {"get_signature": { "name": community_name }}})

    return ctx
