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


def prevent_duplicate_signup(backend, strategy, is_new=False, *args, **kwargs):
    cancel = not (isinstance(backend, UsernameAuth) or isinstance(backend, EmailAuth))
    cancel = cancel or 'disallow_existing' not in strategy.request.params
    if cancel:
        return

    if not is_new:
        raise UserExistsException(backend)


# fork of : python social auth pipeline with the same name: social/pipeline/user.py
def user_details(strategy, details, is_new=False, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user and is_new:
        changed = False  # flag to track changes
        protected = ('username', 'id', 'pk', 'email') + \
            tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

        # Update user model attributes with the new data sent by the current
        # provider. Update on some attributes is disabled by default, for
        # example username and id fields. It's also possible to disable update
        # on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.
        for name, value in details.items():
            if not hasattr(user, name):
                continue
            current_value = getattr(user, name, None)
            if not current_value or name not in protected:
                changed |= current_value != value
                setattr(user, name, value)

        if changed:
            strategy.storage.user.changed(user)
