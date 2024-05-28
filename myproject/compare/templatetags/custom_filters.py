from django import template

register = template.Library()

@register.filter
def length(value):
    return len(value)

@register.filter
def get_range(value):
    return range(len(value))

@register.filter
def get_item(sequence, position):
    return sequence[position]
