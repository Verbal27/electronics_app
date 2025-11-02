from django.views.generic import DetailView
from src.core.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return super().get_queryset().select_related("subcategory")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        if product.subcategory_id:  # type: ignore
            related_qs = (
                Product.objects.filter(subcategory_id=product.subcategory_id)  # type: ignore
                .exclude(pk=product.pk)
                .order_by("-id")[:4]
            )
        else:
            related_qs = Product.objects.none()

        context["related_products"] = related_qs
        return context
