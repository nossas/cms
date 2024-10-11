import pytest
from django.template import Context, Template

from ..templatetags.social_media_tags import url_parse, render_social_media

@pytest.mark.parametrize(
    "input_url, social_media_type, expected",
    [
        ("https://x.com/testuser", "x", "https://x.com/testuser"),
        ("http://instagram.com/testuser", "instagram", "https://instagram.com/testuser"),
        ("www.facebook.com/testuser", "facebook", "https://facebook.com/testuser"),
        ("linkedin.com/in/testuser", "linkedin", "https://linkedin.com/in/testuser"),
        ("https://medium.com/@testuser", "medium", "https://medium.com/@testuser"),
        ("vimeo.com/testuser", "vimeo", "https://vimeo.com/testuser"),
    ],
)
def test_url_parse(input_url, social_media_type, expected):
    assert url_parse(input_url, social_media_type) == expected

@pytest.mark.parametrize(
    "input_url, expected_kind, expected_url",
    [
        ("https://instagram.com/testuser", "instagram", "https://instagram.com/testuser"),
        ("http://www.facebook.com/testuser", "facebook", "https://facebook.com/testuser"),
        ("linkedin.com/in/testuser", "linkedin", "https://linkedin.com/in/testuser"),
        ("https://x.com/testuser", "x", "https://x.com/testuser"),
        ("http://www.instagram.com/testuser", "instagram", "https://instagram.com/testuser"),
        ("https://unknown.com/testuser", None, None),
    ],
)
def test_render_social_media(input_url, expected_kind, expected_url):
    context = render_social_media(input_url)
    assert context.get("kind") == expected_kind
    assert context.get("url") == expected_url


def test_template_render_social_media():
    template = Template(
        '{% load social_media_tags %}{% render_social_media url %}'
    )

    context = Context({"url": "linkedin.com/in/testuser"})
    rendered = template.render(context)
    
    assert 'https://linkedin.com/in/testuser' in rendered

    context = Context({"url": "instagram.com/testuser"})
    rendered = template.render(context)
    
    assert 'https://instagram.com/testuser' in rendered
