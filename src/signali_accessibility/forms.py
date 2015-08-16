from django import forms


class VisibilityColoredStyleFormMixin(object):
    STYLE_CHOICES = (
        ('purple', 'Purple'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('blue', 'Blue'),
        ('red', 'Red'),
    )
    style = forms.ChoiceField(choices=STYLE_CHOICES)