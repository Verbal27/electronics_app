from src.core.components.base import RenderComponentMixin, MediaDefiningComponent


class OrderCard(RenderComponentMixin, MediaDefiningComponent):
    template_name = "components/cabinet/order_card.html"

    class Media:
        css = {
            'all': ('css/components/order_card.css',)
        }

    def __init__(self, request, order, css_classes=None):
        self.request = request
        self.order = order
        self.css_classes = css_classes or ""

    def get_context(self):
        return {
            "order": self.order,
            "items": self.order.items.all(),
            "payment": self.order.payment,
            "css_classes": self.css_classes,
        }
