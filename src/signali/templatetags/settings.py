from django import template
from ..utils import setting
from restful.templatetags.restful import jsonify

register = template.Library()
register.simple_tag(setting)


@register.simple_tag
def setting_json(name):
    return jsonify(setting(name))
