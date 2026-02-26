from decimal import Decimal
from statistics import mean

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView

from src.core.components.website.cards import ProductCard
from src.core.components.website.icon import Icon
from src.core.components.website.span import Span
from src.core.models import Product
from src.core.models.product import ProductReview
from src.website.forms.cart import AddToCartDetailForm
from src.website.forms.checkout import BuyNowForm
from src.website.forms.product_detail import ReviewForm
from src.website.services import CartService


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_breadcrumb(self):
        product = self.object
        return [
            {"label": "Home", "url": reverse("homepage")},
            {
                "label": product.subcategory.category.name,
                "url": product.subcategory.category.get_absolute_url(),
            },
            {
                "label": product.name,
                "url": product.get_absolute_url(),
            },
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        service = CartService(self.request)
        current_qty = service.cart.cart.get(str(product.id), {}).get("quantity", 0)

        review_form = ReviewForm(product=product.id)

        reviews = product.reviews.all()

        product_ratings = [review.rating for review in reviews]

        overall_rating = Decimal(mean(product_ratings)).quantize(Decimal(".0")) if product_ratings else None

        stock_css = (
            "text-warning"
            if product.is_low_stock
            else "custom-text-success"
        )

        related_products = (
            Product.objects
            .filter(subcategory__category=product.subcategory.category)
            .exclude(id=product.id)
            .prefetch_related("images")[:2]
        )

        context.update({
            "breadcrumbs": self.get_breadcrumb(),
            "form": AddToCartDetailForm(
                product_id=product.id,
                product=product,
                current_qty=current_qty,
            ),
            "buy_now": BuyNowForm(
                pk=product.id,
                quantity=current_qty or 1,
            ),
            "images": product.images.all(),
            "primary_image": product.image_url,
            "stock_label": Span(
                content=product.stock_status,
                css_classes=stock_css,
            ),
            "stock_icon": Icon(
                icon_type=Icon.TYPES.CHECK,
                css_classes=stock_css,
            ),
            "specs": product.specification.all(),
            "related": [
                ProductCard(
                    request=self.request,
                    product=related,
                    css_classes="default",
                )
                for related in related_products
            ],
            "reviews": product.reviews.all(),
            "reviews_count": product.reviews.count(),
            "review_form": review_form,
            "product_ratings": len(product_ratings),
            "overall_rating": overall_rating,
        })

        return context


class PostReviewView(LoginRequiredMixin, CreateView):
    model = ProductReview
    form_class = ReviewForm

    def get_success_url(self):
        return reverse("product_detail", args=[self.object.product.id])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.product = get_object_or_404(Product, pk=self.kwargs["pk"])
        kwargs["user"] = self.request.user
        kwargs["product"] = self.product.pk
        return kwargs

    def form_valid(self, form):
        try:
            self.model.check_cooldown(
                user=self.request.user,
                product=self.product,
            )
        except ValidationError as e:
            messages.error(self.request, e.message)
            return redirect("product_detail", pk=self.product.pk)

        if not form.errors:
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.product = self.product
                self.object.user = self.request.user
                self.object.save()

                messages.success(self.request, "Review created successfully!")
                return redirect(self.get_success_url())
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            messages.error(self.request, "Something went wrong")
        return super().form_invalid(form)
