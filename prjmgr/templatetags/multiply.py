from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    if value and arg:
        return value * arg
    return None


@register.filter
def division(value, arg):
    if value and arg:
        return value / arg
    return None