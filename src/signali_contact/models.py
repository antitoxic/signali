from copy import copy

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, Avg, Min, Q
from django.template.defaultfilters import slugify

from unidecode import unidecode
from contact.models import BaseContactPoint, ContactPointManager, BaseOrganisation
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin
from contact_feedback.models import ContactPointFeedback, ContactPointFeedbackedMixin, ContactPointFeedbackManager


class SignalContactPointManager(ContactPointManager, VisibilityManagerMixin):

    @staticmethod
    def add_public_requirement(queryset):
        return VisibilityManagerMixin.add_public_requirement(queryset).exclude(Q(slug=None) | Q(slug=""))

    def _transform_criteria_base(self, queryset):
        return self.add_public_requirement(queryset)

    def _apply_criteria_sorting(self, queryset, sorting, score_expression):
        queryset, order_by = super()._apply_criteria_sorting(queryset, sorting, score_expression)
        queryset = queryset.prefetch_related('children')
        sorting_match_found = False

        valid_sorting = [
            'popularity',
            '-popularity',
            '-created_at',
            '-rating',
            '-effectiveness',
            '-accessibility',
            '-last_visited_at'
        ]
        if sorting in valid_sorting:
            sorting_match_found = True
            order_by.insert(0, sorting)

        if sorting_match_found and '-score' in order_by:
            order_by.remove('-score')

        return queryset, order_by


    def get_by_slug(self, slug):
        try:
            query = self.public_base().filter(slug=slug)
            return self.add_prefetch(query).nocache()[0]
        except:
            raise ContactPoint.DoesNotExist()

    def visited_last(self):
        return self.add_prefetch(self.public_base()).order_by('-last_visited_at')

    def added_last(self):
        return self.add_prefetch(self.public_base()).order_by('-created_at')

    def most_effective(self):
        return self.public_base().order_by('-effectiveness')

    def most_accessible(self):
        return self.public_base().order_by('-accessibility')

    def rated_best(self):
        return self.public_base().order_by('-rating')

    @staticmethod
    def add_prefetch(queryset):
        return queryset.select_related('organisation', 'category') \
            .prefetch_related('keywords')


class SignalOrganisationManager(models.Manager, VisibilityManagerMixin):
    pass


class Organisation(BaseOrganisation, SignalVisibilityMixin):
    objects = SignalOrganisationManager()


class ContactPoint(BaseContactPoint, SignalVisibilityMixin, ContactPointFeedbackedMixin):
    objects = SignalContactPointManager()
    parent = models.ForeignKey('self', related_name='children', null=True)
    visits = models.PositiveIntegerField(_('visits'), default=0)
    anonymous_visits = models.PositiveIntegerField(_('anonymous visits'), default=0)
    last_visited_at = models.DateTimeField(_('created at'), null=True, blank=True)

    def precalculate_feedback_stats(self, feedback_list=None):
        if self.parent is None:
            children = self.children.filter(feedback_count__gt=0)
            if children.count() == 0:
                return
            stats = children.aggregate(
                rating=Avg('rating'),
                effectiveness=Avg('effectiveness'),
                accessibility=Avg('accessibility'),
                feedback_count=Sum('feedback_count'),
            )
            for stat, value in stats.items():
                setattr(self, stat, round(value))
        else:
            super().precalculate_feedback_stats(feedback_list)

    def has_single_child(self):
        return self.children.count() == 1

    @property
    def is_parent_with_many_children(self):
        return self.parent is None and not self.has_single_child()

    @property
    def slug_or_child_slug(self):
        if self.parent:
            return self.slug
        return self.children.all()[0].slug

    def clone(self):
        keywords = self.keywords.all()
        clone = copy(self)
        clone.pk = None
        clone.save()
        clone.keywords = keywords
        return clone

    def get_synced_copy_of_parent(self, parent):
        if self.parent is None:
            return
        # reference fields that differ
        pk = self.id
        area = self.operational_area
        url = self.url
        source_url = self.source_url
        description = self.description
        email = self.email
        # clone parent
        child = copy(parent)
        # apply fields that differ
        child.id = pk
        child.parent = parent
        child.operational_area = area
        child.source_url = source_url
        child.url = url
        child.description = description
        child.email = email
        child.slug = '{}-{}'.format(child.slug, slugify(unidecode(child.operational_area.title)))
        child.save()
        child.keywords = parent.keywords.all()
        return child

    def aggregate_children_visibility(self):
        stats = self.children.aggregate(
            last_visited_at=Min('last_visited_at'),
            visits=Avg('visits'),
            anonymous_visits=Avg('anonymous_visits'),
            popularity=Avg('popularity'),
            views=Avg('views'),
        )
        for stat, value in stats.items():
            if stat != 'last_visited_at':
                value = round(value)
            setattr(self, stat, value)

    def save(self, update_parent=True, *args, **kwargs):
        if update_parent and self.parent is not None:
            self.parent.precalculate_feedback_stats()
            self.parent.aggregate_children_visibility()
            self.parent.save()
        super().save(*args, **kwargs)


class ContactPointGrouped(ContactPoint):
    class Meta:
        proxy = True
        verbose_name = _('Grouped contact point')
        verbose_name_plural = _('Contact point groups')

    def save(self, *args, **kwargs):
        super().save(update_parent=False, *args, **kwargs)


class SignaliContactPointFeedbackManager(ContactPointFeedbackManager):
    pass

class SignalContactPointFeedback(ContactPointFeedback):
    objects = SignaliContactPointFeedbackManager()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('contact-point', kwargs={"slug": self.contactpoint.slug})
