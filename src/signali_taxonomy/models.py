from taxonomy.models import BaseCategory, CategoryManager, BaseKeyword
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin

class SignalCategoryManager(CategoryManager, VisibilityManagerMixin):
    def root_categories_plus_children(self):
        return self.add_children_prefetch(
            self.add_public_requirement(
                self.filter(parent__isnull=True)
            ))


class Category(BaseCategory, SignalVisibilityMixin):
    objects = SignalCategoryManager()

class Keyword(BaseKeyword, SignalVisibilityMixin):
    pass
