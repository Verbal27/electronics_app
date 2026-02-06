from django.urls import reverse
from django.views.generic import DetailView

from src.core.components.website.cards import ProductCard
from src.core.components.website.icon import Icon
from src.core.components.website.span import Span
from src.core.models import Product
from src.website.forms.cart import AddToCartDetailForm
from src.website.forms.checkout import BuyNowForm
from src.website.services import CartService


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_breadcrumb(self):
        product = self.object
        return [
            {"label": "Home", "url": reverse("homepage")},
            {
                "label": product.subcategory.category.name,
                "url": product.subcategory.category.get_absolute_url(),
            },
            {
                "label": product.name,
                "url": product.get_absolute_url(),
            },
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        service = CartService(self.request)
        current_qty = service.cart.cart.get(str(product.id), {}).get("quantity", 0)

        stock_label_content = product.stock_status
        stock_css = (
            "text-warning"
            if stock_label_content == "Low Stock"
            else "custom-text-success"
        )

        related_products = (
            Product.objects
            .filter(subcategory__category=product.subcategory.category)
            .exclude(id=product.id)
            .prefetch_related("images")[:2]
        )

        context.update({
            "breadcrumbs": self.get_breadcrumb(),
            "form": AddToCartDetailForm(
                product_id=product.id,
                product=product,
                current_qty=current_qty,
            ),
            "buy_now": BuyNowForm(
                pk=product.id,
                quantity=current_qty or 1,
            ),
            "images": product.images.all(),
            "primary_image": product.primary_image,
            "stock_label": Span(
                content=stock_label_content,
                title=stock_label_content,
                css_classes=stock_css,
            ),
            "stock_icon": Icon(
                icon_type=Icon.TYPES.CHECK,
                css_classes=stock_css,
            ),
            "specs": product.specification.all(),
            "related": [
                ProductCard(
                    request=self.request,
                    product=related,
                    css_classes="default",
                )
                for related in related_products
            ],
        })

        return context
