from django.dispatch import receiver
from contact.signals import pre_sorting, pre_criteria
from contact.models import ContactPoint

@receiver(pre_sorting, sender=ContactPoint)
def visibility_sorting(sender, queryset, sorting, **kwargs):
    pass
    try:
        if sorting == 'popularity':
            return queryset.order_by('visibility__popularity')
    except KeyError:
        return

@receiver(pre_criteria, sender=ContactPoint)
def visibility_preload(sender, queryset, **kwargs):
    return queryset.select_related('visibility')