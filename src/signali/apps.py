from contact import apps as conttactapps


class ContactConfig(conttactapps.ContactConfig):
    name = 'contact'

    def ready(self):
        super().ready()
        from .signals import handlers

    def init_setting_loader(self):
        from .utils import setting
        conttactapps.setting = setting
