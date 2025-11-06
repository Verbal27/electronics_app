from django.views.generic import ListView
from src.core.models import Product


class HomePageListView(ListView):
    model = Product
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context


class CategoryListView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["pk"]
        return Product.objects.filter(subcategory__category_id=category_id)


class SubCategoryProductListView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"

    def get_queryset(self):
        subcategory_id = self.kwargs["pk"]
        return Product.objects.filter(subcategory_id=subcategory_id)
