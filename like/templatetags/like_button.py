from django import template
register = template.Library()

@register.inclusion_tag('like-button.html')
def like_button(pin_id):
    return {'pin_id': pin_id}
