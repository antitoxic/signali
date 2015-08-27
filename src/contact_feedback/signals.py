import django.dispatch

"""
Dispatched after submitting feedback.
The sender is the new saved instance.
Handlers are not expected a return value.
"""
post_submit = django.dispatch.Signal(providing_args=["feedback"])