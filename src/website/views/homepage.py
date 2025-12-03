from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import ListView, View

from src.core.models import Product, Subcategory
from src.core.components.website.cards import ProductCard
from src.website.forms.cart import AddToCartForm
from src.website.forms.newsletter import NewsletterForm
from src.website.forms.search import Search


class HomePageListView(ListView):
    model = Product
    form_class = AddToCartForm
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            context["hero_product"] = latest
        except Product.DoesNotExist:
            context["hero_product"] = None
        categories_obj = Subcategory.objects.filter()
        context["subcategs"] = [
            {
                "category_name": categories_obj[0].name,
                "id": categories_obj[0].id,
                "icon": "fa-solid fa-mobile",
                "text_color": "text-first",
                "bg_color": "bg-first"
             },
            {
                "category_name": categories_obj[1].name,
                "id": categories_obj[1].id,
                "icon": "fa-solid fa-clock",
                "text_color": "text-second",
                "bg_color": "bg-second"
            },
            {
                "category_name": categories_obj[2].name,
                "id": categories_obj[2].id,
                "icon": "fa-solid fa-tablet",
                "text_color": "text-third",
                "bg_color": "bg-third"
            },
            {
                "category_name": categories_obj[3].name,
                "id": categories_obj[3].id,
                "icon": "fa-solid fa-coffee",
                "text_color": "text-fourth",
                "bg_color": "bg-fourth"
            },
            {
                "category_name": categories_obj[4].name,
                "id": categories_obj[4].id,
                "icon": "fa-solid fa-tablet",
                "text_color": "text-fifth",
                "bg_color": "bg-fifth"
            },
            {
                "category_name": categories_obj[5].name,
                "id": categories_obj[5].id,
                "icon": "fa-solid fa-tv",
                "text_color": "text-sixth",
                "bg_color": "bg-sixth"
            },
        ]
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
            products_qs = Product.objects.filter(name__icontains=query)  # filter by name
            products = [
                ProductCard(request=request, product=p, css_classes="default") for p in products_qs
            ]

        context = {
            "search_form": form,
            "products": products,
            "query": form.cleaned_data.get("query", "") if form.is_valid() else ""
        }
        return render(request, "products.html", context)
