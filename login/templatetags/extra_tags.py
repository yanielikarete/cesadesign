from django import template
from django.core import urlresolvers
import re

register = template.Library()

@register.simple_tag
def active(request, url, return_value='active'):
    resolved = ''
    try:
        resolved = urlresolvers.resolve(request.path)
    except:
        pass
    url = "^%s$" % url
    if re.search(url, resolved.url_name):
        return return_value
    return ''