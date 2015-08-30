from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def update_local_uid(instance, **kwargs):
    instance.social_auth.filter(provider='email').update(uid=instance.email)
