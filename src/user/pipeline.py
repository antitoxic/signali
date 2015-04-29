from django.shortcuts import redirect

from social.pipeline.partial import partial
from social.backends.email import EmailAuth
from social.backends.username import UsernameAuth

@partial
def signupcheckpoint(strategy, details, is_new=False, *args, **kwargs):
    if not is_new:
        return

    if strategy.session_get('saved_email'):
        details['email'] = strategy.session_pop('saved_email')
        details['fullname'] = fullname = strategy.session_pop('saved_name')
        fullname = fullname.split(' ', 1)
        details['first_name'] = fullname[0]
        details['last_name'] = fullname[1]
    else:
        return redirect('user:signup-checkpoint')


def save_checkpoint_changes(is_new=False, *args, **kwargs):
    if not is_new:
        return
