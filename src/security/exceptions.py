from social.exceptions import AuthException
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class WrongPasswordAuthException(AuthException):
    def __str__(self):
        return _('Invalid password')


class UserExistsAuthException(AuthException):
    def __str__(self):
        return _('User already exists')


class UserDoesNotExistAuthException(AuthException, UserModel.DoesNotExist):
    def __str__(self):
        return _('Such user does not exist')
