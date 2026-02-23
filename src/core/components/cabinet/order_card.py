from electronics_app.settings import COUNT_IMAGE
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

    def count_itmes(self, count=0):
        for item in self.order.items.all():
            count += 1
        return count

    def get_context(self):
        return {
            "order": self.order,
            "show_items": self.order.items.all()[:5],
            "more_to_show": self.count_itmes() - 5,
            "count_image": COUNT_IMAGE,
            "all_items": self.order.items.all(),
            "count": self.count_itmes(),
            "payment": self.order.payment,
            "css_classes": self.css_classes,
        }
