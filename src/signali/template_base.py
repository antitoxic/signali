from django.template import Node, TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _


class AssignableGetterNode(Node):
    def __init__(self, getter, setting_name, context_varname=None):
        self.getter = getter
        self.setting_name = setting_name
        self.context_varname = context_varname

    def render(self, context):
        setting_name = self.setting_name.resolve(context)
        value = self.getter(setting_name)
        if self.context_varname is None:
            return value
        context[self.context_varname] = value
        return ''


def getter_tag_factory(getter):
    def getter_tag(parser, token):
        try:
            bits = token.split_contents()
        except ValueError:
            raise TemplateSyntaxError(_("Can't split content"))

        setting_name = parser.compile_filter(bits[1])
        if len(bits) == 2:
            return AssignableGetterNode(getter, setting_name)
        if len(bits) != 4 and bits[2] != 'as':
            raise TemplateSyntaxError(_("Invalid `setting` tag format"))
        return AssignableGetterNode(getter, setting_name, bits[3])

    return getter_tag
