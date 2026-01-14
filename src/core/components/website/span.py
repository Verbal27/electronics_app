from src.core.components.base import RenderComponentMixin, MediaDefiningComponent
from django.utils.safestring import mark_safe


class Span(RenderComponentMixin, MediaDefiningComponent):
    template_name = "components/website/span.html"

    def __init__(self, content=None, id=None, css_classes='', content_mark_safe=False, **kwargs):
        self.content = mark_safe(content) if content_mark_safe else content
        self.id = id
        self.css_classes = css_classes
        self.content_mark_safe = content_mark_safe
        self.data_attributes = kwargs

    def get_context(self):
        return {
            "content": self.content,
            "id": self.id,
            "css_classes": self.css_classes,
            "content_mark_safe": self.content_mark_safe,
            "data_attributes": self.data_attributes,
        }
