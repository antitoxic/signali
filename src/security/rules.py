import rules

@rules.predicate
def is_same_person(user, target_user):
    return user == target_user