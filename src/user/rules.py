import rules
from security.rules import is_same_person

@rules.predicate
def is_active_and_validated_user(user):
    return user.is_active and user.is_email_validated

@rules.predicate
def is_not_stuff(user):
    return not user.is_staff

rules.add_perm('user.profile_view', is_same_person | rules.is_staff)
rules.add_perm('user.profile_change', is_same_person | rules.is_staff)
