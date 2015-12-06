from django.template import Library

from restful.templatetags.restful import jsonify

from ..utils import setting
from ..template_base import getter_tag_factory

register = Library()

"""
Retrieves a setting
{% setting 'name' %} -> outputs
{% setting 'name' as site_name %} -> sets variable
"""
register.tag('setting', getter_tag_factory(setting))

@register.simple_tag
def setting_json(name):
    return jsonify(setting(name))
