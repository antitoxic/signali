from ..models import Category
from django import template

register = template.Library()

@register.inclusion_tag('_categories_menu.html', takes_context=True)
def categories_menu(context):
    return {
        "categories": Category.objects.filter(parent__isnull=True).prefetch_related('children'),
        "request": context.get('request')
    }

@register.inclusion_tag('taxonomy/_picker.html', takes_context=True)
def taxonomy_picker(context):
    return {
        "categories": Category.objects.filter(parent__isnull=True).prefetch_related('children'),
        "request": context.get('request')
    }
