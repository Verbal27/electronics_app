from src.core.components.base import RenderComponentMixin


class Icon(RenderComponentMixin):
    template_name = "components/website/icon.html"

    class TYPES:
        EDIT = "fas fa-pen"
        DELETE = "fas fa-trash"
        PROMO = "fas fa-tag"
        CHECKOUT = "fa-solid fa-arrow-right"
        BAG = "fa-solid fa-shopping-bag"

    def __init__(self, icon_type, css_classes=None, css_style=None):
        self.icon_type = icon_type
        self.css_classes = css_classes
        self.css_style = css_style

    def get_context(self):
        return {
            "icon_type": self.icon_type,
            "css_classes": self.css_classes,
            "css_style": self.css_style,
        }
