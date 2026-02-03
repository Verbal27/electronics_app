from src.core.components.website.cards import ProductCard
from src.core.components.website.icon import Icon
from src.core.components.website.span import Span
from src.website.forms.checkout import BuyNowForm
from src.website.services import CartService
from src.website.forms.cart import AddToCartDetailForm
from django.views.generic import DetailView
from src.core.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    form_class = AddToCartDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        service = CartService(self.request)
        current_qty = service.cart.cart.get(str(product.id), {}).get("quantity", 0)
        stock_label_content = product.stock_status
        stock_label_css_classes = ("text-warning" if stock_label_content == "Low Stock" else "custom-text-success")

        related_products = (
            Product.objects
            .filter(subcategory__category=product.subcategory.category)
            .exclude(id=product.id)
            .prefetch_related("images")
            [:2]
        )

        specs = product.specification.all()

        context["related"] = [
            ProductCard(request=self.request, product=product, css_classes="default") for product in related_products
        ]

        context.update({
            "breadcrumbs": product.get_breadcrumb(),
            "form": self.form_class(
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
                css_classes=stock_label_css_classes,
            ),
            "stock_icon": Icon(
                icon_type=Icon.TYPES.CHECK,
                css_classes=stock_label_css_classes,
            ),
            "specs": specs
        })

        return context
