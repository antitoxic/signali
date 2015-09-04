from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from social.pipeline.partial import partial
from social.exceptions import AuthException
from social.backends.legacy import LegacyAuth

from .forms import SignUpCheckpointForm


@partial
def signupcheckpoint(strategy, details, is_new=False, *args, **kwargs):
    if not is_new:
        return

    if strategy.session_get('saved_email'):
        details['email'] = strategy.session_pop('saved_email')
        details['fullname'] = fullname = strategy.session_pop('saved_name')
        details['first_name'], details['last_name'] = fullname.split(' ', 1)
    else:
        return redirect('user:signup-checkpoint')


def parse_user_data(backend, details, social, *args, **kwargs):
    if not (isinstance(backend, LegacyAuth) and social is None):
        return

    form = SignUpCheckpointForm(data=details)
    if not form.is_valid():
        raise AuthException(_("Invalid data provided"))
    details.update(form.cleaned_data)
    return {
        "details": details
    }
