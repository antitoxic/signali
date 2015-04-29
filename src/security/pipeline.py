from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from social.backends.email import EmailAuth
from social.backends.username import UsernameAuth

from .exceptions import WrongPasswordException, UserExistsException
from .forms import SetPasswordForm


def user_password(backend, strategy, user=None, is_new=False, *args, **kwargs):
    if not (isinstance(backend, UsernameAuth) or isinstance(backend, EmailAuth)):
        return

    if is_new:
        form = SetPasswordForm(strategy.request.params)
        if not form.is_valid():
            raise WrongPasswordException(backend)
        password = form.cleaned_data['new_password1']
        return {
            "hashed_password": make_password(password)
        }
    elif not user.check_password(strategy.request.params.get('password')):
        raise WrongPasswordException(backend)


def save_password(backend, user=None, is_new=False, *args, **kwargs):
    if not is_new or not (isinstance(backend, UsernameAuth) or isinstance(backend, EmailAuth)):
        return

    if 'hashed_password' in kwargs:
        user.password = kwargs['hashed_password']
        user.save()
    else:
        raise WrongPasswordException(backend)


def load_user(strategy, *args, **kwargs):
    UserModel = get_user_model()
    try:
        return {
            "user": UserModel.objects.get(email=strategy.request.params.get('email'))
        }
    except Exception:
        return None


def prevent_duplicate_signup(backend, strategy, is_new=False, *args, **kwargs):
    cancel = not (isinstance(backend, UsernameAuth) or isinstance(backend, EmailAuth))
    cancel = cancel or 'disallow_existing' not in strategy.request.params
    if cancel:
        return

    if not is_new:
        raise UserExistsException(backend)
