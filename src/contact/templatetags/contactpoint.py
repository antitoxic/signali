from django import template

register = template.Library()

@register.inclusion_tag('_stats.html', takes_context=True)
def contactpoint_stats(context):
    pass