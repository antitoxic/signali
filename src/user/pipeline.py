from django.shortcuts import redirect
from social.pipeline.partial import partial

@partial
def signupcheckpoint(strategy, details, is_new=False, *args, **kwargs):
    if not is_new:
        return

    if strategy.session_get('saved_email'):
        details['email'] = strategy.session_pop('saved_email')
        name = strategy.session_pop('saved_name').split(' ', 1)
        details['first_name'] = name[0]
        details['last_name'] = name[1]
    else:
        return redirect('user:signup-checkpoint')


def save_checkpoint_changes(is_new=False, *args, **kwargs):
    if not is_new:
        return
