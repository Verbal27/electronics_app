from electronics_app.settings import PRODUCT_PLACEHOLDER_IMAGE
from src.core.utils.subcategory_list import list_subcategories
from src.core.components.website.cards import ProductCard
from src.website.forms.newsletter import NewsletterForm
from src.website.forms.cart import AddToCartForm
from django.views.generic import ListView, View
from django.shortcuts import redirect, render
from src.website.forms.search import Search
from django.contrib import messages
from src.core.models import Product
from django.db.models import Sum


class HomePageListView(ListView):
    model = Product
    form_class = AddToCartForm
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["placeholder_image"] = PRODUCT_PLACEHOLDER_IMAGE
        featured = Product.objects.annotate(
            total_sold=Sum("orderitem__quantity")
        ).order_by("-total_sold", "-created_at")[:4]
        context['featured'] = [
            ProductCard(request=self.request, product=product, css_classes="default") for product in featured
        ]
        trending = Product.objects.annotate(
            total_sold=Sum("orderitem__quantity")
        ).order_by("-total_sold", "-created_at")[:3]
        context["trending"] = [
            ProductCard(request=self.request, product=product, css_classes="large") for product in trending
        ]
        try:
            latest = Product.objects.latest("created_at")
            context["hero_image"] = (
                latest.images.filter(is_primary=True).first() or latest.images.first()
            )
            context["hero_product"] = latest
        except Product.DoesNotExist:
            context["hero_product"] = None
        context["subcategories"] = list_subcategories(self.request)
        return context


class SubscribeView(View):

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Temporally print email, in future use it for sending emails middleware
            print(email)
            messages.success(self.request, "Thank you for subscribing!")
        else:
            messages.error(self.request, "Please enter a valid email.")
        return redirect("homepage")


class SearchView(View):
    template_name = "products.html"

    def get(self, request):
        form = Search(request.GET or None)
        products = []
        products = Product.objects.none()

        if form.is_valid():
            query = form.cleaned_data["query"]
            products_qs = Product.objects.filter(name__icontains=query)
            products = [
                ProductCard(request=request, product=p, css_classes="default") for p in products_qs
            ]

        context = {
            "search_form": form,
            "products": products,
            "query": form.cleaned_data.get("query", "") if form.is_valid() else ""
        }
        return render(request, "products.html", context)
