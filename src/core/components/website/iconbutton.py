from src.core.components.base import RenderComponentMixin, MediaDefiningComponent
from src.core.components.website.icon import Icon


class IconButton(RenderComponentMixin, MediaDefiningComponent):
    template_name = "components/website/icon_button.html"

    class Media:
        css = {
            'all': ('css/components/simple_input.css',)
        }

    def __init__(self,
                 name,
                 icon: Icon,
                 css_classes=None,
                 label=None,
                 value=None,
                 css_style=None,
                 icon_css_classes=None
                 ):
        self.name = name
        self.value = value
        self.label = label
        self.icon = icon
        self.css_classes = css_classes
        self.css_style = css_style
        self.icon_css_classes = icon_css_classes

    def get_context(self):
        return {
            "name": self.name,
            "value": self.value,
            "label": self.label,
            "css_classes": self.css_classes,
            "css_style": self.css_style,
            "icon": self.icon,
            "icon_css_classes": self.icon_css_classes,
        }
