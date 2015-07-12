from django.conf import settings
from .models import Setting


def setting(name):
    try:
        return getattr(settings, name)
    except:
        site_settings = Setting.objects.all()[:1].get()
        return getattr(site_settings, name, None)
