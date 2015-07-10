from contact import apps


class ContactConfig(apps.ContactConfig):
    name = 'contact'

    def init_setting_loader(self):
        from siteguide.utils import setting
        apps.setting = setting
