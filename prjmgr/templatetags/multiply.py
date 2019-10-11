from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    if arg:
        return value * arg
    return None