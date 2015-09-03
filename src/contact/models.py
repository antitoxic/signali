from django.db import models
from django.utils.translation import ugettext_lazy as _

from .apps import setting

class ContactPointManager(models.Manager):
    def apply_criteria(self, filters, sorting):
        queryset = self.all()
        try:
            queryset = self._transform_criteria_base(queryset)
        except AttributeError:
            pass
        queryset = queryset.filter(filters)
        queryset = self._apply_criteria_sorting(queryset, sorting)
        return queryset

    def get_by_slug(self, slug):
        return self.get(slug=slug)

    def _apply_criteria_sorting(self, queryset, sorting):
        return queryset.order_by(sorting)


class BaseContactPoint(models.Model):
    class Meta:
        abstract = True
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
    url = models.URLField(_('URL'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    operational_area = models.ForeignKey(setting('CONTACT_AREA_MODEL', noparse=True), related_name="contact_points", verbose_name=_("operational area"))

    organisation = models.ForeignKey(setting('CONTACT_ORGANISATION_MODEL', noparse=True), related_name="contact_points", verbose_name=_("organisation"))
    keywords = models.ManyToManyField(setting('CONTACT_KEYWORD_MODEL', noparse=True), related_name="contact_points", verbose_name=_("keywords"))
    category = models.ForeignKey(setting('CONTACT_CATEGORY_MODEL', noparse=True), related_name="contact_points", verbose_name=_("category"))

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

    def __str__(self):
        return self.title



class BaseOrganisation(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('organisation')
        verbose_name_plural = _('organisations')
    address = models.OneToOneField(setting('CONTACT_AREA_MODEL', noparse=True), blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('title'), max_length=250, blank=False)
    email = models.EmailField(_('email'), max_length=250, blank=False)
    operational_area = models.ForeignKey(setting('CONTACT_AREA_MODEL', noparse=True),
                                         related_name="organisations",
                                         verbose_name=_("operational area"),
                                         blank=True,
                                         null=True,
                                         on_delete=models.SET_NULL)

    def __str__(self):
        return '{} ({})'.format(self.title, self.email)
