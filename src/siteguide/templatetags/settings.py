from django import template
from ..utils import setting

register = template.Library()
register.simple_tag(setting)
