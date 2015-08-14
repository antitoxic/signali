from django.conf import settings
from .models import Setting
import importlib

def setting(name, default=None):
    try:
        value = getattr(settings, name, default)
    except:
        site_settings = Setting.objects.all()[:1].get()
        value = getattr(site_settings, name, default)

    if name in settings.CLASS_SETTINGS:
        module, value = value.rsplit('.', 1)
        module = importlib.import_module(module)
        value = getattr(module, value, default)

    return value