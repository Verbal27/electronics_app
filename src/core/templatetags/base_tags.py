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
