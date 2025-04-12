from django import template
import os

register = template.Library()

@register.filter
def normalize_ext(value):
    base, ext = os.path.splitext(value)
    return base + ext.lower()