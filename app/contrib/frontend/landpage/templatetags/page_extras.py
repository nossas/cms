from django import template

from contrib.bonde.models import Community

register = template.Library()


# @register.inclusion_tag("frontend/landpage/plugins/footer.html")
# def show_footer(styles=None, community_name=None, **kwargs):
#     ctx = kwargs

#     if styles:
#         ctx.update({"instance": {"styles": styles}})

#     if community_name:
#         ctx.update({"community": {"get_signature": { "name": community_name }}})

#     return ctx


@register.inclusion_tag("frontend/landpage/plugins/footer.html", takes_context=True)
def render_bonde_footer(context):
    request = context["request"]

    community = Community.objects.on_site(request).first()
    return {"community": community}
