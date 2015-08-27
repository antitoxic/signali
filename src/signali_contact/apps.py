from contact import apps as conttactapps
from contact_feedback import apps as feedbackapps


class ContactConfig(conttactapps.ContactConfig):
    name = 'contact'

    def __init__(self, *args, **kwargs):
        from signali.utils import setting
        conttactapps.setting = setting
        super().__init__(*args, **kwargs)



class FeedbackConfig(feedbackapps.FeedbackConfig):
    name = 'contact_feedback'

    def __init__(self, *args, **kwargs):
        from signali.utils import setting
        feedbackapps.setting = setting
        super().__init__(*args, **kwargs)
