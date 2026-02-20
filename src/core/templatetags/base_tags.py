from django import template
from django.utils.safestring import mark_safe

from src.core.components.base import MediaDefiningComponentClass

register = template.Library()


@register.simple_tag
def component_js():
    return mark_safe(''.join({component.render_js() for component in MediaDefiningComponentClass.components}))


@register.simple_tag
def component_css():
    return mark_safe(''.join([component.render_css() for component in MediaDefiningComponentClass.components]))


@register.simple_tag(takes_context=True)
def is_active(context, *url_names):
    request = context['request']
    if request.resolver_match:
        current_url_name = request.resolver_match.url_name
        if current_url_name in url_names:
            return "active-tab"
    return ""
