from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    def get_avatar(self, uid=None):
        if self.avatar:
            src = settings.MEDIA_URL + self.avatar.url()
        else:
            uid = settings.SOCIAL_AUTH_FACEBOOK_KEY
            if hasattr(self, 'preloaded_uid'):
                uid = self.preloaded_uid
            elif self.social_auth.all().count() > 0:
                uid = self.social_auth.all()[0].uid
            src = self.get_facebook_avatar(uid)
        return src

    @staticmethod
    def get_facebook_avatar(uid):
        return 'http://graph.facebook.com/' + uid + '/picture'
