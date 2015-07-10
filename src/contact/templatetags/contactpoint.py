from django import template
from ..models import Organisation
from location.models import Area
from ..apps import setting

register = template.Library()

@register.inclusion_tag('_stats.html')
def contactpoint_stats():
    return {
        "organisations_count": Organisation.objects.all().count(),
        "areas_count": Area.objects.exclude(size__in=[setting('contact_address_areasize')]).count(),
    }