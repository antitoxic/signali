from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

def user_file_name(instance, filename):
    return '/'.join(['user', filename])


class User(AbstractUser):
    avatar = models.ImageField(_('avatar'), upload_to=user_file_name, blank=True, null=True)
    is_email_validated = models.BooleanField(_('Is email validated'), default=True,
        help_text=_('Designates whether this user has validated '
                    'their email.'))

    @property
    def is_valid(self):
        return self.is_active and self.is_email_validated

    def get_avatar(self, uid=None):
        if self.avatar:
            src = settings.MEDIA_URL + self.avatar.url()
        else:
            try:
                uid = self.preloaded_uid
            except:
                uid = settings.SOCIAL_AUTH_FACEBOOK_KEY
            try:
                uid = self.social_auth.get(provider='facebook').uid
            except:
                pass
            src = self.get_facebook_avatar(uid)
        return src

    @staticmethod
    def get_facebook_avatar(uid):
        return 'http://graph.facebook.com/' + uid + '/picture'
