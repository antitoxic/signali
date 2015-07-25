import django.dispatch

"""
Dispatched before sorting querysets for any of the models.
Handlers should return queryset object or `None`.
"""
pre_sorting = django.dispatch.Signal(providing_args=["queryset"])
"""
Dispatched before appying user filtering criteria
to querysets for any of the models.
Handlers should return queryset object or `None`.
"""
pre_criteria = django.dispatch.Signal(providing_args=["queryset"])
"""
Dispatched when picking class for form validation.
Handlers should return form class or `None`.
"""
criteria_validation = django.dispatch.Signal(providing_args=["form"])