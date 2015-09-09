from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .models import ContactPoint, SignalContactPointFeedback

UserModel = get_user_model()

def publish_user_first_feedback_per_contactpoint(user):
    for point in ContactPoint.objects.filter(feedback__user=user):
        first_feedback = point.feedback.filter(user=user).order_by('added_at')[0]
        if first_feedback.is_public:
            continue
        first_feedback.is_public = True
        first_feedback.save()

@receiver(post_save, sender=UserModel)
def sync_activation_with_user(instance, **kwargs):
    if not instance.is_active:
        SignalContactPointFeedback.objects.filter(user=instance, is_active=True).update(is_active=False)
    elif instance.is_email_validated:
        publish_user_first_feedback_per_contactpoint(instance)


