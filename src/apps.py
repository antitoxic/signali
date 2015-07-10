from contact import apps as conttactapps


class ContactConfig(conttactapps.ContactConfig):
    name = 'contact'

    def init_setting_loader(self):
        from siteguide.utils import setting
        conttactapps.setting = setting
