from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplies two numbers in the template.
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
