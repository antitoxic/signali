from django import template
from taxonomy.models import Category

register = template.Library()

@register.inclusion_tag('_popular_categories.html', takes_context=True)
def popular_categories(context):
    return {
        "categories": Category.objects.all().order_by('visibility__popularity', 'visibility__is_featured')[:13],
        "request": context.get('request')
    }
