import django.dispatch

"""
Dispatched after user visits a contactpoint website.
The sender is the contactpoint class .
Handlers are not expected a return value.
"""
post_visit = django.dispatch.Signal(providing_args=["contactpoint", "user"])
