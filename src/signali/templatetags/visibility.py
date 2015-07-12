from django import template
from taxonomy.models import Category
from ..models import Visibility

register = template.Library()

@register.inclusion_tag('_popular_categories.html', takes_context=True)
def popular_categories(context):
    return {
        "categories": Category.objects
                              .all()
                              .extra(select={'is_featured': Visibility._meta.db_table + '.is_featured OR NULL'})
                              .order_by('visibility__popularity', 'is_featured')[:13],
        "request": context.get('request')
    }
