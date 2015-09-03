import django.dispatch

"""
Dispatched after submitting proposal for a new contact point.
The sender is the class of the new saved instance.
Handlers are not expected a return value.
"""
post_submit = django.dispatch.Signal(providing_args=["contactpoint"])