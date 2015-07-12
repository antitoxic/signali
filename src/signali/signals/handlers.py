from django.dispatch import receiver
from contact.signals import pre_sorting
from contact.models import ContactPoint

@receiver(pre_sorting, sender=ContactPoint)
def my_handler(sender, queryset, criteria):
    try:
        if criteria['sorting'] == 'popularity':
            return queryset.order_by('visibility__popularity')
    except KeyError:
        return