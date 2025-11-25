from django.views.generic import DetailView

from src.core.models import Product
from src.website.forms.cart import AddToCartDetailForm


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    form_class = AddToCartDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["related_products"] = product
        context["form"] = self.form_class(product_id=product.id)
        return context
