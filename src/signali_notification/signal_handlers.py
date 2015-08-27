from contact_feedback.signals import post_submit as post_submit_feedback
from django.dispatch import receiver
from notification import email
from django.conf import settings

@receiver(post_submit_feedback)
def new_feedback_to_admin(feedback, *args, **kwargs):
    pass
    # email.send('notification/new_feedback', settings.ADMIN_EMAIL)
