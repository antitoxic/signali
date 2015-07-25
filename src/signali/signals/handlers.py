from django.dispatch import receiver
from contact.signals import pre_sorting, pre_criteria
from contact.models import ContactPoint

@receiver(pre_sorting, sender=ContactPoint)
def visibility_sorting(sender, queryset, criteria):
    try:
        if criteria['sorting'] == 'popularity':
            return queryset.order_by('visibility__popularity')
    except KeyError:
        return

@receiver(pre_criteria, sender=ContactPoint)
def visibility_filter(sender, queryset, criteria):
    try:
        return queryset.filter(visibility__is_featured=criteria['is_featured'])
    except KeyError:
        return