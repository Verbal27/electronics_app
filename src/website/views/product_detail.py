from django.views.generic import DetailView

from src.core.models import Product
from src.website.forms.cart import AddToCartDetailForm
from src.website.services.cart_services import CartService


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

        context["form"] = self.form_class(
            product_id=product.id,
            product=product,
            current_qty=current_qty
        )
        return context
