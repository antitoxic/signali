import django.dispatch

"""
Dispatched before sorting querysets for any of the models
Handlers should return queryset object or None
"""
pre_sorting = django.dispatch.Signal(providing_args=["queryset"])