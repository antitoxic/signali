from contact_feedback.signals import post_submit as post_submit_feedback
from signali_contact.signals import post_visit
from django.dispatch import receiver
from .models import Subscriber
from notification import email
from django.conf import settings

@receiver(post_submit_feedback)
def new_feedback_to_admin(feedback, *args, **kwargs):
    pass
    # email.send('notification/new_feedback', settings.ADMIN_EMAIL)


@receiver(post_visit)
def subscribe_after_visit(contactpoint, user, *args, **kwargs):
    if user is None or not user.is_authenticated():
        return
    s = Subscriber(contactpoint=contactpoint, user=user)
    s.save()
