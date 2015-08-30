from django.contrib.auth.hashers import make_password

from social.backends.legacy import LegacyAuth

from .exceptions import WrongPasswordAuthException, UserExistsAuthException, UserDoesNotExistAuthException
from .forms import SetPasswordForm


def user_password(backend, strategy, user=None, is_new=False, *args, **kwargs):
    if not isinstance(backend, LegacyAuth):
        return

    if is_new:
        form = SetPasswordForm(strategy.request.POST)
        if not form.is_valid():
            raise WrongPasswordAuthException(backend)
        password = form.cleaned_data['new_password1']
        return {
            "hashed_password": make_password(password)
        }
    elif not user.check_password(strategy.request.POST.get('password')):
        raise WrongPasswordAuthException(backend)


def save_password(backend, user=None, is_new=False, *args, **kwargs):
    if not is_new or not isinstance(backend, LegacyAuth):
        return

    try:
        user.password = kwargs['hashed_password']
    except:
        raise WrongPasswordAuthException(backend)

    user.save()


def prevent_duplicate_signup_on_register(backend, strategy, user=None, *args, **kwargs):
    if not (isinstance(backend, LegacyAuth) and strategy.request.params.get('auth_type') == 'login'):
        return

    if user is not None:
        raise UserExistsAuthException(backend)


def refuse_missing_user_on_login(backend, strategy, user=None, *args, **kwargs):
    if not (isinstance(backend, LegacyAuth) and strategy.request.params.get('auth_type') == 'registration'):
        return

    if user is None:
        raise UserDoesNotExistAuthException(backend)


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
            try:
                current_value = getattr(user, name)
            except:
                continue
            if not current_value or name not in protected:
                changed |= current_value != value
                setattr(user, name, value)

        if changed:
            strategy.storage.user.changed(user)
