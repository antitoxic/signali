from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse


from social.backends.legacy import LegacyAuth
from social.pipeline.user import USER_FIELDS


from .exceptions import WrongPasswordAuthException, UserExistsAuthException, UserDoesNotExistAuthException
from .forms import SetPasswordForm

UserModel = get_user_model()

def user_password(backend, strategy, social, user=None, *args, **kwargs):
    if not isinstance(backend, LegacyAuth):
        return

    if social is None:
        form = SetPasswordForm(strategy.request.POST)
        if not form.is_valid():
            raise WrongPasswordAuthException(backend)
        password = form.cleaned_data['new_password1']
        return {
            "hashed_password": make_password(password)
        }
    elif not user.check_password(strategy.request.POST.get('new_password1')):
        raise WrongPasswordAuthException(backend)


def save_password(backend, social, user=None, *args, **kwargs):
    if not (social is None and isinstance(backend, LegacyAuth)):
        return

    try:
        user.password = kwargs['hashed_password']
    except:
        raise WrongPasswordAuthException(backend)

    user.save()


def local_user(backend, uid, user=None, *args, **kwargs):
    if user is not None:
        return

    try:
        return {
            "user": UserModel.objects.get(email=uid),
            "is_new": False
        }
    except:
        pass


def prevent_duplicate_on_register(backend, social, strategy, *args, **kwargs):
    if not (isinstance(backend, LegacyAuth) and strategy.request.params.get('auth_type') == 'registration'):
        return

    if social is not None:
        raise UserExistsAuthException(backend)


def refuse_missing_user_on_login(backend, social, strategy, *args, **kwargs):
    if not (isinstance(backend, LegacyAuth) and strategy.request.params.get('auth_type') == 'login'):
        return

    if social is None:
        raise UserDoesNotExistAuthException(backend)


# fork of : python social auth pipeline with the same name: social/pipeline/user.py
def user_details(strategy, details, is_new, user=None, *args, **kwargs):
    """Fill missing user details using data from current provider."""
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
            if not current_value and name not in protected:
                changed |= current_value != value
                setattr(user, name, value)

        if changed:
            strategy.storage.user.changed(user)


# fork of : python social auth pipeline with the same name: social/pipeline/user.py
def create_user(strategy, backend, details, is_new, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    if not fields:
        return

    requires_validation = backend.REQUIRES_EMAIL_VALIDATION or \
                          backend.setting('FORCE_EMAIL_VALIDATION', False)
    if is_new and requires_validation:
        fields["is_email_validated"] = False
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }



def send_email_validation(backend, details, user=None, *args, **kwargs):
    requires_validation = backend.REQUIRES_EMAIL_VALIDATION or \
                          backend.setting('FORCE_EMAIL_VALIDATION', False)

    send_validation = bool(details.get('email')) and not user.is_email_validated
    if requires_validation and send_validation:
        backend.strategy.session_set('email_validation_address', details.get('email'))
        backend.strategy.session_set(REDIRECT_FIELD_NAME,
                                     reverse('security:email-validation-sent'))
        backend.strategy.send_email_validation(backend, details['email'])


