from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .apps import setting
from signali_taxonomy.models import Keyword

class ContactPointManager(models.Manager):
    def apply_criteria(self, score_expression, filters, sorting):
        queryset = self.all()
        try:
            queryset = self._transform_criteria_base(queryset)
        except NotImplementedError:
            pass
        queryset = queryset.filter(filters)
        if score_expression != 0:
            queryset = queryset.annotate(score=score_expression)
            queryset = queryset.order_by(*self._get_criteria_sorting(queryset, sorting, score_expression))
        return queryset

    def get_by_slug(self, slug):
        return self.get(slug=slug)

    def _get_criteria_sorting(self, queryset, sorting, score_expression):
        return ['-score'] if score_expression != 0 else []

    """
    Called before applying criteria with user filters
    """
    def _transform_criteria_base(self, queryset):
        raise NotImplementedError("Your subclcass must implement this")


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
    notes = models.TextField(_('notes'), blank=True)
    operational_area = models.ForeignKey(setting('CONTACT_AREA_MODEL', noparse=True), related_name="contact_points", verbose_name=_("operational area"))
    proposed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="contactpoint_proposals", verbose_name=_("user that proposed it"), null=True, blank=True)

    organisation = models.ForeignKey(setting('CONTACT_ORGANISATION_MODEL', noparse=True), related_name="contact_points", verbose_name=_("organisation"), null=True)
    keywords = models.ManyToManyField(setting('CONTACT_KEYWORD_MODEL', noparse=True), related_name="contact_points", verbose_name=_("keywords"))
    category = models.ForeignKey(setting('CONTACT_CATEGORY_MODEL', noparse=True), related_name="contact_points", verbose_name=_("category"))

    # features
    is_multilingual = models.CharField(_('is multilingual'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW, blank=True)
    is_response_guaranteed = models.CharField(_('guarantees response'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW, blank=True)
    is_verifiable = models.CharField(_('is verifiable'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW, blank=True)
    is_confirmation_issued = models.CharField(_('is there a confirmation issued'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW, blank=True)
    is_mobile_friendly = models.CharField(_('is mobile friendly'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW, blank=True)
    is_final_destination = models.CharField(_('is final destination'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW, blank=True)
    is_anonymous_allowed = models.CharField(_('allows anonymous requests'), max_length=20, choices=EXTENDED_BOOLEAN_CHOICES, default=DONTKNOW, blank=True)

    # requirements
    is_registration_required = models.BooleanField(_('required registration'), default=False, blank=True)
    is_photo_required = models.BooleanField(_('photo registration'), default=False, blank=True)
    is_esign_required = models.BooleanField(_('required e-signature'), default=False, blank=True)
    is_name_required = models.BooleanField(_('required name'), default=False, blank=True)
    is_email_required = models.BooleanField(_('required email'), default=False, blank=True)
    is_pic_required = models.BooleanField(_('required personal indentification code'), default=False, blank=True)
    is_address_required = models.BooleanField(_('required address'), default=False, blank=True)
    is_location_required = models.BooleanField(_('required location'), default=False, blank=True)

    def __str__(self):
        return "{} ({})".format(self.title, str(self.category))



class BaseOrganisation(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('organisation')
        verbose_name_plural = _('organisations')
    address = models.OneToOneField(setting('CONTACT_AREA_MODEL', noparse=True), blank=True, null=True, on_delete=models.SET_NULL, parent_link=True)
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
