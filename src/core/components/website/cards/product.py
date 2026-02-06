from electronics_app.settings import PRODUCT_PLACEHOLDER_IMAGE
from src.core.components.base import RenderComponentMixin, MediaDefiningComponent
from src.website.forms.cart import AddToCartForm
from django.urls import reverse


class ProductCard(RenderComponentMixin, MediaDefiningComponent):
    template_name = "components/website/product_card.html"
    form_class = AddToCartForm

    class Media:
        css = {
            'all': ('css/components/product_card.css',)
        }

    def __init__(self, request, product, form_class=None, css_classes=None):
        self.product = product
        self.css_classes = css_classes or ""
        self.request = request
        self.form_class = form_class or self.form_class
        self.form = self.form_class(product_id=product.id)

    def get_context(self):
        return {
            "product": self.product,
            "product_name": self.product.name,
            "product_description": self.product.description,
            "product_price": self.product.price,
            "product_image_url": self.product.image.url if self.product.image else PRODUCT_PLACEHOLDER_IMAGE,
            "product_subcategory": self.product.subcategory,
            "product_detail_url": reverse("product_detail", args=[self.product.pk]),
            "css_classes": self.css_classes,
            "form": self.form,
        }
