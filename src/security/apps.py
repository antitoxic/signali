from django.apps import AppConfig

class SecurityConfig(AppConfig):
    name = "security"
    verbose_name = "Taking care once and for all for all auth"

    def ready(self):
        from . import signal_handlers
