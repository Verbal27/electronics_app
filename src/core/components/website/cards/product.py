from django.urls import reverse
from src.core.components.base import RenderComponentMixin, MediaDefiningComponent


class ProductCard(RenderComponentMixin, MediaDefiningComponent):
    template_name = "components/website/product_card.html"

    class Media:
        css = {
            'all': ('css/components/product_card.css',)
        }

    def __init__(self, product, css_classes=None):
        self.product = product
        self.css_classes = css_classes or ""

    def get_context(self):
        return {
            "product": self.product,
            "product_name": self.product.name,
            "product_description": self.product.description,
            "product_price": self.product.price,
            "product_image_url": self.product.image.url,
            "product_detail_url": reverse("product_detail", args=[self.product.pk]),
            "css_classes": self.css_classes,
        }
