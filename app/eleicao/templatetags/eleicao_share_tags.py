import re
from django import template

register = template.Library()

pattern = re.compile(
    r"(?:https?:\/\/)?(?:www.)?(?:twitter|medium|facebook|vimeo|instagram)(?:.com\/)?([@a-zA-Z0-9-_]+)"
)


@register.filter
def url_parse(value: str, social_media_type):
    """Parse social media URL to standardize"""
    urls = {
        "twitter": "https://twitter.com/",
        "instagram": "https://instagram.com/",
        "facebook": "https://facebook.com/",
    }
    base_url = urls.get(social_media_type, None)

    result = re.search(pattern, value)

    if result:
        result = result.group(1)

    if not base_url:
        return value

    if result and base_url:
        return f"{base_url}{result}"

    if not result and base_url:
        return f"{base_url}{value}"

    return value
