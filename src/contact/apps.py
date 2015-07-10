from django.apps import AppConfig

setting = None

missing_setting_warning = """
Please ensure this module has a `setting` attribute (a function) that
is responsible for retrieving app-specific settings.

Best way to do this is to extend the config class and override the
setting initialisation method
"""

class ContactConfig(AppConfig):
    verbose_name = "Managing contact points of organisations"

    def ready(self):
        self.init_setting_loader()
        if setting is None:
            raise ImportError(missing_setting_warning)

    def init_setting_loader(self):
        pass