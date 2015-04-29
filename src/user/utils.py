from security.utils import get_validation_url
from notification import email


def send_validation(strategy, backend, code):
    url = get_validation_url(strategy, backend, code)
    email.send('user/account_validation_email', code.email, url=url)
