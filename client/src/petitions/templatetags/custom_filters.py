from django import template
from django.utils.encoding import force_str
from base64 import b64encode

from django.template.defaulttags import register


@register.filter
def b_64encode(value):
    """
    Encodes a string to base64 format.
    """
    value = force_str(value)
    return b64encode(value.encode("utf-8")).decode("utf-8")
