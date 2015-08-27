import rules

@rules.predicate
def is_feedback_author(user, feedback):
    return user == feedback.user

rules.add_perm('contact.feedback_create', is_feedback_author | rules.is_staff)
