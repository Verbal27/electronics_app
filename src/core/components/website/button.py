from src.core.components.base import RenderComponentMixin


class Button(RenderComponentMixin):
    template_name = "components/website/button.html"

    class Styles:
        PRIMARY = "btn-primary"
        OUTLINE_PRIMARY = 'btn-outline-primary'
        OUTLINE_SECONDARY = 'btn-outline-secondary'
        INFO = 'btn-info'
        SECONDARY = "btn-secondary"
        LINK = "btn-link"
        DARK = "btn-dark"

    def __init__(
            self,
            label,
            style=Styles.PRIMARY,
            type="button",
            icon=None,
            url=None,
            id=None,
            css_class=None,
            label_classes=''
    ):
        self.label = label
        self.label_classes = label_classes
        self.style = style
        self.type = type
        self.icon = icon
        self.url = url
        self.id = id
        self.css_class = css_class

    def get_context(self):
        return {
            "label": self.label,
            "label_classes": self.label_classes,
            "style": self.style,
            "type": self.type,
            "icon": self.icon,
            "url": self.url,
            "id": self.id,
            "css_class": self.css_class,
        }
