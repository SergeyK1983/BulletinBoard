from django import template
from django.conf import settings


register = template.Library()

media_url = settings.MEDIA_URL


@register.simple_tag()
def get_media_prefix():
    return media_url
