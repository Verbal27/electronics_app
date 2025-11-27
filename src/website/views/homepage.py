from django.db.models import Sum
from django.views.generic import ListView

from src.core.components.website.inputs import SimpleInput
from src.core.models import Product, Subcategory
from src.core.components.website.cards import ProductCard
from src.website.forms.cart import AddToCartForm
from src.website.forms.search import Search


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
        trending = Product.objects.annotate(
            total_sold=Sum("orderitem__quantity")
        ).order_by("-total_sold", "-created_at")[:4]
        context['trending'] = [
            ProductCard(request=self.request, product=product) for product in trending
        ]
        try:
            latest = Product.objects.latest("created_at")
            context["hero_product"] = latest
        except Product.DoesNotExist:
            context["hero_product"] = None
        context['search_bar'] = SimpleInput(
            name='search',
            placeholder="Search items"
        )
        context['search_btn'] = Search()
        categories_obj = Subcategory.objects.filter()
        context["categs"] = [
            {"category_name": categories_obj[0].name, "icon": "fa-solid fa-computer"},
            {"category_name": categories_obj[1].name, "icon": "fa-solid fa-mobile"},
            {"category_name": categories_obj[2].name, "icon": "fa-solid fa-tv"},
            {"category_name": categories_obj[3].name, "icon": "fa-solid fa-tv"},
            {"category_name": categories_obj[4].name, "icon": "fa-solid fa-tv"},
            {"category_name": categories_obj[5].name, "icon": "fa-solid fa-tv"},
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
