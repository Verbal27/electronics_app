from electronics_app.settings import COUNT_IMAGE
from src.core.components.base import RenderComponentMixin, MediaDefiningComponent


class OrderCard(RenderComponentMixin, MediaDefiningComponent):
    template_name = "components/cabinet/order_card.html"

    MAX_VISIBLE_ITEMS = 5

    class Media:
        css = {
            "all": ("css/components/order_card.css",)
        }

    def __init__(self, request, order, css_classes=None):
        self.request = request
        self.order = order
        self.css_classes = css_classes or ""

    def get_context(self):
        items = self.order.items.all()

        total_count = len(items)
        visible_items = list(items[:self.MAX_VISIBLE_ITEMS])

        remaining_count = max(total_count - self.MAX_VISIBLE_ITEMS, 0)

        return {
            "order": self.order,
            "show_items": visible_items,
            "more_to_show": remaining_count,
            "count_image": COUNT_IMAGE,
            "all_items": items,
            "count": total_count,
            "payment": self.order.payment,
            "css_classes": self.css_classes,
        }
