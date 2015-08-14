from django.db import models
from django.utils.translation import ugettext_lazy as _
from .signals import pre_sorting, pre_criteria


class ContactPointManager(models.Manager):
    def apply_criteria(self, filters, sorting):
        queryset = self.all()

        enriched_querysets = pre_criteria.send(sender=ContactPoint, queryset=queryset)
        for receiver, q in enriched_querysets:
            try:
                queryset = q & queryset
            except AttributeError:
                pass

        queryset = queryset.filter(filters)

        sorted_querysets = pre_sorting.send(sender=ContactPoint, queryset=queryset, sorting=sorting)
        sorted_querysets = [q for receiver, q in sorted_querysets if q is not None]
        try:
            queryset = sorted_querysets[0]
        except IndexError:
            queryset = queryset.order_by(sorting)

        return queryset

class ContactPoint(models.Model):
    class Meta:
        verbose_name = _('contact point')
        verbose_name_plural = _('contact points')

    objects = ContactPointManager()

    YES = 'yes'
    NO = 'no'
    DONTKNOW = 'dontknow'
    EXTENDED_BOOLEAN_CHOICES = (
        (YES, _('Yes')),
        (NO, _('No')),
        (DONTKNOW, _("I don't know")),
    )

    title = models.CharField(_('title'), max_length=250, blank=False)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    operational_area = models.ForeignKey('location.Area', related_name="contact_points", verbose_name=_("operational area"))

    organisation = models.ForeignKey('Organisation', related_name="contact_points", verbose_name=_("organisation"))
    keywords = models.ManyToManyField('taxonomy.Keyword', related_name="contact_points", verbose_name=_("keywords"))
    category = models.ForeignKey('taxonomy.Category', related_name="contact_points", verbose_name=_("category"))
    response_time = models.PositiveIntegerField(_('response time'), max_length=20, blank=True, null=True)
    ratings = models.ManyToManyField('feedback.Rating', verbose_name=_("Ratings"), through='ContactPointRating')

    # features
    is_multilingual = models.CharField(_('is multilingual'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_response_guaranteed = models.CharField(_('guarantees response'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_verifiable = models.CharField(_('is verifiable'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_confirmation_issued = models.CharField(_('is there a confirmation issued'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_mobile_friendly = models.CharField(_('is mobile friendly'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_final_destination = models.CharField(_('is final destination'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)
    is_anonymous_allowed = models.CharField(_('allows anonymous requests'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW)

    # requirements
    is_registration_required = models.BooleanField(_('required registration'), default=False)
    is_photo_required = models.BooleanField(_('photo registration'), default=False)
    is_esign_required = models.BooleanField(_('required e-signature'), default=False)
    is_name_required = models.BooleanField(_('required name'), default=False)
    is_email_required = models.BooleanField(_('required email'), default=False)
    is_pic_required = models.BooleanField(_('required personal indentification code'), default=False)
    is_address_required = models.BooleanField(_('required address'), default=False)
    is_location_required = models.BooleanField(_('required location'), default=False)

    @property
    def rating_usability(self):
        for r in self.ratings.all():
            if r.rating.criteria == ContactPointRating.RATING_KEY_USABILITY:
                return r

    def __str__(self):
        return self.title


class ContactPointRating(models.Model):
    RATING_KEY_USABILITY = 'usability'
    RATING_KEY_RESPONSE_SPEED = 'speed'
    RATING_TYPE_CHOICES = (
        (RATING_KEY_USABILITY, _('Usability')),
        (RATING_KEY_RESPONSE_SPEED, _('Response speed')),
    )

    class Meta:
        unique_together = [('contactpoint', 'rating')]
    contactpoint = models.ForeignKey('ContactPoint', related_name='skills_portfolio')
    rating = models.ForeignKey('feedback.Rating', related_name='talents_portfolio')
    criteria_guide = models.TextField(_("What is this rating indicating?."), blank=True, null=True)



class Organisation(models.Model):
    address = models.OneToOneField('location.Area', blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('title'), max_length=250, blank=False)
    email = models.EmailField(_('email'), max_length=250, blank=False)
    operational_area = models.ForeignKey('location.Area',
                                         related_name="organisations",
                                         verbose_name=_("operational area"),
                                         blank=True,
                                         null=True,
                                         on_delete=models.SET_NULL)

    def __str__(self):
        return '{} ({})'.format(self.title, self.email)
