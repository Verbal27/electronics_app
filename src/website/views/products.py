from django.urls import reverse

from src.core.components.website.cards import ProductCard
from django.views.generic import ListView
from src.core.models import Product, Category, Subcategory


class ProductsListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "products.html"

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        products = context.get("products", Product.objects.all())
        context["product_cards"] = [
            ProductCard(request=self.request, product=product) for product in products
        ]
        context["breadcrumbs"] = [
            {"label": "Home", "url": reverse("homepage")},
            {"label": "All Products", "url": ""},
        ]
        return context


class CategoryListView(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs["pk"])
        return Product.objects.filter(subcategory__category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context["products"]
        context["product_cards"] = [
            ProductCard(request=self.request, product=product) for product in products
        ]
        context["breadcrumbs"] = self.category.get_breadcrumb()
        return context


class SubCategoryProductListView(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"

    def get_queryset(self):
        self.subcategory = Subcategory.objects.get(pk=self.kwargs["pk"])
        return Product.objects.filter(subcategory=self.subcategory)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["product_cards"] = [
            ProductCard(request=self.request, product=product)
            for product in context["products"]
        ]

        context["breadcrumbs"] = self.subcategory.get_breadcrumb()

        return context
