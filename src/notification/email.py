from django.template import RequestContext
from django.conf import settings
from django.http import HttpRequest
from django.template.loader import get_template
from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection as django_get_connection
from django.utils.translation import ugettext_lazy as _


class MissingConnectionException(Exception):
    pass


def send(templatename_without_ext, to, sender=settings.DEFAULT_FROM_EMAIL, reply_to=settings.DEFAULT_FROM_EMAIL, request=None, internal=False, **kwargs):
    if request is None:
        request = HttpRequest()

    template_context = RequestContext(request, kwargs)

    text_template = get_template(templatename_without_ext+'.txt')
    subject, text = text_template.render(template_context).strip().split("\n", 1)
    subject = subject.strip("\r")

    try:
        html_template = get_template(templatename_without_ext+'.html')
        html = html_template.render(template_context)
    except:
        html = None

    headers = {'Reply-To': reply_to}

    try:
        iter(to)
    except:
        to = [to]

    connection_label = settings.EMAIL_CONNECTION_LABEL_INTERNAL if internal else None
    send_raw(subject, text, sender, to, headers, connection_label, html)


def send_raw(subject, text, sender, to, headers, connection_label=None, html=None):
    connection = get_connection(connection_label)
    if html is None:
        msg = EmailMessage(subject, text, sender, to, headers=headers, connection=connection)
    else:
        msg = EmailMultiAlternatives(subject, text, sender, to, headers=headers, connection=connection)
        msg.attach_alternative(html, "text/html")

    msg.send(fail_silently=False)


def get_connection(label=None, **kwargs):
    if label is None:
        label = settings.EMAIL_CONNECTION_LABEL_PUBLIC

    try:
        connections = settings.EMAIL_CONNECTIONS
        options = connections[label]
    except (KeyError, AttributeError):
        raise MissingConnectionException(
            _('Settings for connection "%(connection_label)s" were not found') % {'label': label}
        )

    options.update(kwargs)
    return django_get_connection(**options)