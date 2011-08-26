from django import template


register = template.Library()

def sub(value, arg):
    "Subtracts the arg from the value"
    try:
        arg = int(arg)
    except TypeError:
        arg = len(arg)
    return value - arg

register.filter('sub', sub)
