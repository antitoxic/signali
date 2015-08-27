import importlib

from django.apps import apps as django_apps
from django.conf import settings
from .models import Setting


def setting(name, default=None, noparse=False):
    try:
        value = getattr(settings, name)
    except:
        site_settings = Setting.objects.all()[:1].get()
        value = getattr(site_settings, name, default)

    if name in settings.MODEL_SETTINGS and not noparse:
        value = django_apps.get_model(value)

    if name in settings.CLASS_SETTINGS and not noparse:
        module, value = value.rsplit('.', 1)
        module = importlib.import_module(module)
        value = getattr(module, value, default)

    return value