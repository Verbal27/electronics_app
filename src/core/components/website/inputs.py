from src.core.components.base import RenderComponentMixin, MediaDefiningComponent


class SimpleInput(RenderComponentMixin, MediaDefiningComponent):
    template_name = "components/website/simple_input.html"

    class Media:
        css = {
            'all': ('css/components/simple_input.css',)
        }

    def __init__(self, name, value="", placeholder="", input_type="text", css_classes=""):
        self.name = name
        self.value = value
        self.placeholder = placeholder
        self.input_type = input_type
        self.css_classes = css_classes

    def get_context(self):
        return {
            "name": self.name,
            "value": self.value,
            "placeholder": self.placeholder,
            "input_type": self.input_type,
            "css_classes": self.css_classes
        }
