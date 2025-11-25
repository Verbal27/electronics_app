from django.views.generic import ListView

from src.core.components.website.inputs import SimpleInput
from src.core.models import Product, Category
from src.core.components.website.cards import ProductCard
from src.website.forms.cart import AddToCartForm


class HomePageListView(ListView):
    model = Product
    form_class = AddToCartForm
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context.get("products", Product.objects.all())
        context["product_cards"] = [
            ProductCard(request=self.request, product=product) for product in products
        ]
        context['search_bar'] = SimpleInput(
            name='search',
            placeholder="Search items"
        )
        categories_obj = Category.objects.filter()
        context['categs'] = [
            {
                'category_name': categories_obj[0].name,
                'icon': 'fas fas-computer'
            },
            {
                'category_name': categories_obj[1].name,
                'icon': 'fas fas-smartphone'
            },
            {
                'category_name': categories_obj[2].name,
                'icon': 'fas fas-smartphone'
            },
        ]
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
        context["product_cards"] = [
            ProductCard(request=self.request, product=product) for product in products
        ]
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
        context["product_cards"] = [
            ProductCard(request=self.request, product=product) for product in products
        ]
        return context
