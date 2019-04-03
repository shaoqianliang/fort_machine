from django import template
register = template.Library()

@register.filter(name='truncate_chars')
def truncate_chars(value):
    return value

#register.filter('truncate_chars', truncate_chars)

