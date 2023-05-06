from django.template import Library
import base64

register = Library()


@register.filter
def b64encode(value):
    return base64.b64encode(value).decode("utf-8")
