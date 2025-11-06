from django.views.generic import ListView
from src.core.models import Product
from src.core.components.website.cards import ProductCard


class HomePageListView(ListView):
    model = Product
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context["product_cards"] = [ProductCard(product) for product in products]
        return context


class CategoryListView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["pk"]
        return Product.objects.filter(subcategory__category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context["products"]
        context["product_cards"] = [ProductCard(product) for product in products]
        return context


class SubCategoryProductListView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"

    def get_queryset(self):
        subcategory_id = self.kwargs["pk"]
        return Product.objects.filter(subcategory_id=subcategory_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context["products"]
        context["product_cards"] = [ProductCard(product) for product in products]
        return context
