import django.dispatch

"""
Dispatched after user is validated.
The sender is the user model class.
Handlers are not expected a return value.
"""
post_email_validation = django.dispatch.Signal(providing_args=["user"])
