from django import template
from ..models import Partner

register = template.Library()

@register.inclusion_tag("partners/partners_list.html")
def show_partners():
    partners = Partner.objects.all()
    return {'partners': partners}
