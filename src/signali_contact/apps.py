from contact import apps as conttactapps


class ContactConfig(conttactapps.ContactConfig):
    name = 'contact'

    def __init__(self, *args, **kwargs):
        from signali.utils import setting
        conttactapps.setting = setting
        super().__init__(*args, **kwargs)
