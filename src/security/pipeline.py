from django.contrib.auth.models import User
from social.backends.email import EmailAuth
from social.backends.username import UsernameAuth
from .exceptions import WrongPasswordException
from django.contrib.auth.hashers import make_password



def user_password(backend, request, response, user=None, is_new=False, *args, **kwargs):
    if not (isinstance(backend, UsernameAuth) or isinstance(backend, EmailAuth)):
        return

    password = request.get('password')
    if is_new:
        return {
            "hashed_password": make_password(password)
        }
    elif not user.check_password(password):
        raise WrongPasswordException(backend)


def save_password(backend, user=None, is_new=False, *args, **kwargs):
    if not is_new or not (isinstance(backend, UsernameAuth) or isinstance(backend, EmailAuth)):
        return

    if 'hashed_password' in kwargs:
        user.password = kwargs['hashed_password']
        user.save()
    else:
        raise WrongPasswordException(backend)


def load_user(request, *args, **kwargs):
    try:
        return {
            "user": User.objects.get(email=request.get('email'))
        }
    except Exception:
        return None