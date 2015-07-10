from django import template

register = template.Library()

@register.inclusion_tag('_user_controls.html', takes_context=True)
def user_controls(context):
    request = context.get('request')
    return {
        "user": request.user,
        "request": request
    }
