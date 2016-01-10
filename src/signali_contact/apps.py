from contact import apps as conttactapps
from contact.search_watson import ContactPointSearchAdapter
from contact_feedback import apps as feedbackapps
from watson import search as watson

class SignaliContactConfig(conttactapps.ContactConfig):
    name = 'signali_contact'

    def ready(self):
        ContactPoint = self.get_model("ContactPoint")
        from . import signal_handlers
        watson.register(ContactPoint, ContactPointSearchAdapter)


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
