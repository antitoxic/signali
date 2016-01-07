from copy import copy

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, Avg, Min, Q
from django.template.defaultfilters import slugify

from unidecode import unidecode
from contact.models import BaseContactPoint, ContactPointManager, BaseOrganisation
from accessibility.models import VisibilityManagerMixin, VisibilityQuerySetMixin
from signali_accessibility.models import SignalVisibilityMixin
from contact_feedback.models import ContactPointFeedback, ContactPointFeedbackedMixin, ContactPointFeedbackManager


class SignalPointQuerySet(models.QuerySet, VisibilityQuerySetMixin):
    def children(self):
        return self.exclude(parent=None)

    def parents(self):
        return self.filter(parent=None)

    def public(self):
        return super().public().exclude(Q(slug=None) | Q(slug=""))

    def visited_last(self):
        return self.public().prefetch().order_by('-last_visited_at')

    def added_last(self):
        return self.public().prefetch().order_by('-created_at')

    def most_effective(self):
        return self.public().prefetch().order_by('-effectiveness')

    def most_accessible(self):
        return self.public().prefetch().order_by('-accessibility')

    def rated_best(self):
        return self.public().prefetch().order_by('-rating')

    def prefetch(self):
        return self.select_related('organisation', 'category', 'operational_area') \
            .prefetch_related('keywords', 'children', 'children__operational_area')


class SignalContactPointManager(ContactPointManager):

    def _transform_criteria_base(self, queryset):
        return queryset.public()

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
            return self.public().filter(slug=slug).prefetch().nocache()[0]
        except:
            raise ContactPoint.DoesNotExist()


class SignalOrganisationManager(models.Manager, VisibilityManagerMixin):
    pass


class Organisation(BaseOrganisation, SignalVisibilityMixin):
    objects = SignalOrganisationManager()


class ContactPoint(BaseContactPoint, SignalVisibilityMixin, ContactPointFeedbackedMixin):
    objects = SignalContactPointManager.from_queryset(SignalPointQuerySet)()
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
        self.precalculate_feedback_stats()
        super().save(*args, **kwargs)

    def title_or_organisation(self):
        specific = self.title
        if not specific:
            specific = self.organisation.title
        return specific

    def full_title(self):
        title = self.title
        if not title:
            title = self.organisation.title
        else:
            title = "{} — {}".format(title, self.organisation.title)
        if self.operational_area and not self.operational_area.is_root_node():
            title = "{} — {}".format(title, self.operational_area.title)
        return title



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
