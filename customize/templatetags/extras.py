from django import template

register = template.Library()

@register.simple_tag
def eur_to_uah(value):
    return f"{value * 51.44:.2f}UAH"

@register.filter
def round_price(value):
    return round(value, 2)

