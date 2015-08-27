from django.apps import AppConfig

class NotificationConfig(AppConfig):
    name = "signali_notification"
    verbose_name = "Sending out notifications according to signals from other apps"

    def ready(self):
        from . import signal_handlers
