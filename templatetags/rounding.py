# app/templatetags/rounding.py

from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def round_down(value, size=1):
    size = Decimal(size)
    return (Decimal(value)//size) * size
