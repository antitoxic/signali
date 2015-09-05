from django import template
register = template.Library()

@register.filter()
def fieldname(instance, form):
    return form.get_instance_html_name(instance)
