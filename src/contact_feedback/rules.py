import rules

@rules.predicate
def is_feedback_author(user, feedback):
    return user == feedback.user

@rules.predicate
def was_first_feedback_for_contactpoint(user, contactpoint):
    return contactpoint.feedback.filter(user=user).count() == 1

rules.add_perm('contact.feedback_create', is_feedback_author | rules.is_staff)
rules.add_perm('contact.feedback_publish', was_first_feedback_for_contactpoint | rules.is_staff)
