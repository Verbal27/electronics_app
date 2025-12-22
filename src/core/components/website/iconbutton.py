from crispy_forms.layout import LayoutObject
from django.template.loader import render_to_string

from src.core.components.website.icon import Icon


class IconButton(LayoutObject):
    template = "components/website/icon_button.html"

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

    def render(self, form, form_style, template_pack=None):
        return render_to_string(
            self.template,
            {
                "name": self.name,
                "value": self.value,
                "label": self.label,
                "css_classes": self.css_classes,
                "css_style": self.css_style,
                "icon": self.icon,
                "icon_css_classes": self.icon_css_classes,
            }
        )
