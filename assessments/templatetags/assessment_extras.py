from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Template filter to get a value from a dictionary using a key.
    Usage: {{ mydict|lookup:mykey }}
    """
    if dictionary and key:
        return dictionary.get(key, '')
    return ''

@register.filter
def get_item(dictionary, key):
    """
    Alternative name for lookup filter.
    Usage: {{ mydict|get_item:mykey }}
    """
    return lookup(dictionary, key) 