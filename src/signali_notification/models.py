from django.db import models
from notification.models import BaseSubscriber

class Subscriber(BaseSubscriber):
    contactpoint = models.ForeignKey('signali_contact.ContactPoint', related_name='subscribers')
