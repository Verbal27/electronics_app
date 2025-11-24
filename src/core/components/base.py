from django.forms.renderers import get_default_renderer
from django.forms.widgets import Media
from django.template.context_processors import csrf
from django.utils.safestring import mark_safe


class RenderComponentMixin:
    request = None

    def get_context(self):
        raise NotImplementedError(
            "Subclasses of RenderableMixin must provide a get_context() method."
        )

    def render(self, template_name=None, context=None, renderer=None):
        renderer = renderer or get_default_renderer()
        template = template_name or self.template_name
        context = context or self.get_context()
        if self.request:
            context["csrf_token"] = csrf(self.request)["csrf_token"]


        return mark_safe(renderer.render(template, context, self.request))

    def no_render(self):
        return self.template_name, self.get_context()

    @classmethod
    def set_request(cls, request):
        cls.request = request

    __str__ = render
    __html__ = render


class MediaDefiningComponentClass(type):
    """
    Metaclass for components that can have media definitions.
    """
    components = []

    @classmethod
    def register_component(cls, new_class):
        cls.components.append(new_class)

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        definition = getattr(new_class, 'Media', None)
        if definition:
            new_class.media = Media(definition)
            MediaDefiningComponentClass.register_component(new_class)
        return new_class


class MediaDefiningComponent(metaclass=MediaDefiningComponentClass):

    @classmethod
    def render_js(cls):
        return ''.join(cls.media.render_js())

    @classmethod
    def render_css(cls):
        return ''.join(cls.media.render_css())
