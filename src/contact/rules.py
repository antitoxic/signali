import rules

@rules.predicate
def is_contactpoint_proposer(user, contactpoint):
    return user == contactpoint.proposed_by

rules.add_perm('contact.contactpoint_create', is_contactpoint_proposer | rules.is_staff)
