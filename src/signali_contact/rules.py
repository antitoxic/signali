import rules
from contact_feedback.rules import was_first_feedback_for_contactpoint
from user.rules import is_active_and_validated_user, is_not_stuff
from security.rules import rate_limit_by_cookie, rate_limit_by_ip, rate_limit_by_user

rules.remove_perm('contact.feedback_publish')
rules.add_perm(
    'contact.feedback_publish',
    (is_active_and_validated_user & was_first_feedback_for_contactpoint) | rules.is_staff
)

rules.add_perm(
    'contact.visit',
    is_not_stuff
    # USER: 1 every 15 minutes if user is logged in
    & rate_limit_by_user("contact.visit", limit=1, seconds=60*15)
    # COOKIE: 1 every hour if user is not logged in
    & rate_limit_by_cookie("contact.visit", limit=1, seconds=60*60)
    # IP: 1 every 3 minutes if user is not logged in (broader than cookie as we are not aware how many people share 1 ip)
    & rate_limit_by_ip("contact.visit", limit=1, seconds=60*3)
)
