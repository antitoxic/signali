import rules
from contact_feedback.rules import was_first_feedback_for_contactpoint
from user.rules import is_active_and_validated_user

rules.remove_perm('contact.feedback_publish')
rules.add_perm(
    'contact.feedback_publish',
    (is_active_and_validated_user & was_first_feedback_for_contactpoint) | rules.is_staff
)
