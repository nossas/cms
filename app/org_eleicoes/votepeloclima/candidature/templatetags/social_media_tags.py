import re
from django import template

register = template.Library()

pattern = re.compile(
    r"(?:https?:\/\/)?(?:www\.)?(?:x|medium|facebook|linkedin\.com\/in|vimeo|instagram)(?:\.com\/)?(?:in\/)?@?([a-zA-Z0-9-_.]+)"
)

def url_parse(value: str, social_media_type):
    """Parse social media URL to standardize"""
    urls = {
        "x": "https://x.com/",
        "instagram": "https://instagram.com/",
        "facebook": "https://facebook.com/",
        "linkedin": "https://linkedin.com/in/",
    }
    base_url = urls.get(social_media_type, None)

    result = re.search(pattern, value)

    if result:
        result = result.group(1)

    if not result or not base_url:
        if not value.startswith("http://") and not value.startswith("https://"):
            value = "https://" + value
        return value

    if result and base_url:
        return f"{base_url}{result}"

    return value


@register.inclusion_tag("candidature/templatetags/social_media.html")
def render_social_media(url):
    if url and "instagram" in url:
        return {"url": url_parse(url, "instagram"), "kind": "instagram"}
    elif url and "facebook" in url:
        return {"url": url_parse(url, "facebook"), "kind": "facebook"}
    elif url and "linkedin" in url:
        return {"url": url_parse(url, "linkedin"), "kind": "linkedin"}
    elif url and "x" in url:
        return {"url": url_parse(url, "x"), "kind": "x"}
    

    return {}
