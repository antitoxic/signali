from taxonomy.models import BaseCategory, CategoryManager, BaseKeyword
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin

class SignalCategoryManager(CategoryManager, VisibilityManagerMixin):
    pass


class Category(BaseCategory, SignalVisibilityMixin):
    objects = SignalCategoryManager()

class Keyword(BaseKeyword, SignalVisibilityMixin):
    pass