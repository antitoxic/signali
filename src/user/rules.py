import rules
from security.rules import is_same_person

rules.add_perm('user.profile_view', is_same_person | rules.is_staff)
rules.add_perm('user.profile_change', is_same_person | rules.is_staff)