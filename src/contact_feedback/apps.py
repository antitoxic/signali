from django.apps import AppConfig

setting = None

missing_setting_warning = """
Please ensure this module has a `setting` attribute (a callable) that
is responsible for retrieving app-specific settings.

Best way to do this is to extend the config class and override the
setting initialisation method
"""

class FeedbackConfig(AppConfig):
    verbose_name = "Managing contact point's feedback"

    def ready(self):
        if setting is None:
            raise ImportError(missing_setting_warning)
