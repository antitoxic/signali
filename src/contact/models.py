from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _


class ContactPoint(models.Model):
    class Meta:
        verbose_name = _('contact point')
        verbose_name_plural = _('contact points')

    YES = 'yes'
    NO = 'no'
    DONTKNOW = 'dontknow'
    EXTENDED_BOOLEAN_CHOICES = (
        (YES, _('Yes')),
        (NO, _('No')),
        (DONTKNOW, _("I don't know")),
    )
    RATING_KEY_USABILITY = 'usability'
    RATING_KEY_RESPONSE_SPEED = 'speed'

    title = models.CharField(_('title'), max_length=250, blank=False)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    response_time = models.PositiveIntegerField(_('response time'), max_length=20, blank=True, null=True)
    is_multilingual = models.CharField(_('is multilingual'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_response_guaranteed = models.CharField(_('guarantees response'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_verifiable = models.CharField(_('is verifiable'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_confirmation_issued = models.CharField(_('is there a confirmation issued'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_mobile_friendly = models.CharField(_('is mobile friendly'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_final_destination = models.CharField(_('is final destination'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_anonymous_allowed = models.CharField(_('allows anonymous requests'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)

    is_registration_required = models.BooleanField(_('required registration '), default=False)
    is_photo_required = models.BooleanField(_('photo registration '), default=False)
    is_esign_required = models.BooleanField(_('required e-signature'), default=False)
    is_name_required = models.BooleanField(_('required name'), default=False)
    is_email_required = models.BooleanField(_('required email'), default=False)
    is_pic_required = models.BooleanField(_('required personal indentification code'), default=False)
    is_address_required = models.BooleanField(_('required address'), default=False)
    is_location_required = models.BooleanField(_('required location'), default=False)

    organisation = models.ForeignKey('Orgаnisation', related_name="contact_points", verbose_name=_("organisation"))
    keywords = models.ManyToManyField('taxonomy.Keyword', related_name="contact_points", verbose_name=_("keywords"))
    category = models.ForeignKey('taxonomy.Category', related_name="contact_points", verbose_name=_("category"))
    rating_usability = GenericRelation('rating.Rating', related_query_name='contact_points')
    rating_response_speed = GenericRelation('rating.Rating', related_query_name='contact_points')


class ContactPointRequirement(models.Model):
    class Meta:
        verbose_name = _('contact point requirement')
        verbose_name_plural = _('contact point requirements')
    title = models.CharField(_('title'), max_length=250, blank=False)
    contact_point = models.ForeignKey('ContactPoint', related_name="requirements", verbose_name=_("contact point"))

class Orgаnisation(models.Model):
    title = models.CharField(_('title'), max_length=250, blank=False)
    email = models.EmailField(_('email'), max_length=250, blank=False)
    address = models.TextField(_('address'), blank=True)
    city = models.TextField(_('city'), blank=True)