from django.db.models import QuerySet

from taxonomy.models import BaseCategory, CategoryQuerySetMixin, BaseKeyword
from accessibility.models import VisibilityQuerySetMixin
from signali_accessibility.models import SignalVisibilityMixin

class CategoryQuerySet(QuerySet, CategoryQuerySetMixin, VisibilityQuerySetMixin):
    def non_empty(self):
        return self.filter(contact_points=None)

class Category(BaseCategory, SignalVisibilityMixin):
    objects = CategoryQuerySet.as_manager()


class Keyword(BaseKeyword, SignalVisibilityMixin):
    pass
