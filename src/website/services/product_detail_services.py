from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

from electronics_app import settings
from src.core.models import Product, OrderItem
from src.core.components.website.cards import ProductCard
from src.core.components.website import Icon, Span
from src.core.models.product_review import ProductReview
from src.website.forms.cart import AddToCartDetailForm
from src.website.forms.checkout import BuyNowForm
from src.website.forms.product_detail import ReviewForm
from src.website.services import CartService


class ProductDetailService:
    def __init__(self, request, product: Product):
        self.request = request
        self.product = product
        self.cart_service = CartService(request)

    def get_breadcrumbs(self):
        return [
            {"label": "Home", "url": reverse("homepage")},
            {
                "label": self.product.subcategory.category.name,
                "url": self.product.subcategory.category.get_absolute_url(),
            },
            {
                "label": self.product.name,
                "url": self.product.get_absolute_url(),
            },
        ]

    def get_cart_quantity(self):
        return self.cart_service.cart.cart.get(str(self.product.id), {}).get("quantity", 0)

    def get_review_form(self):
        return ReviewForm(product=self.product)

    def get_reviews_page(self, page=1, per_page=5):
        reviews = (
            self.product.approved_reviews
            .select_related("user")
            .with_verified_purchase()
            .order_by("-created_at")
        )
        paginator = Paginator(reviews, per_page)
        page_obj = paginator.get_page(page)
        return page_obj, paginator.count

    def get_stock_info(self):
        css = "text-warning" if self.product.is_low_stock else "custom-text-success"
        return {
            "label": Span(content=self.product.stock_status, css_classes=css),
            "icon": Icon(icon_type=Icon.TYPES.CHECK, css_classes=css),
        }

    @staticmethod
    def check_cooldown(user):
        last_review = (
            ProductReview.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if not last_review:
            return

        now = timezone.now()
        cooldown_until = last_review.created_at + settings.REVIEW_COOLDOWN

        if now < cooldown_until:
            remaining = cooldown_until - now
            minutes = int(remaining.total_seconds() // 60)

            raise ValidationError(
                f"You can review again in {minutes} minutes."
            )

    def get_user_review(self):
        if not self.request.user.is_authenticated:
            return None

        return (
            self.product.approved_reviews
                .filter(user=self.request.user)
                .with_verified_purchase()
                .first()
        )

    def get_related_products(self, limit=2):
        related_products = (
            Product.objects
            .filter(subcategory__category=self.product.subcategory.category)
            .exclude(id=self.product.id)
            .prefetch_related("images")[:limit]
            .select_related("subcategory__category")
        )
        return [
            ProductCard(request=self.request, product=related, css_classes="default")
            for related in related_products
        ]

    def get_rating_distribution(self):
        ratings = (
            self.product.approved_reviews
            .values("rating")
            .annotate(count=Count("rating"))
        )

        rating_map = {r["rating"]: r["count"] for r in ratings}

        total = sum(rating_map.values())

        distribution = []

        for star in range(5, 0, -1):
            count = rating_map.get(star, 0)
            percent = (count / total * 100) if total else 0

            distribution.append({
                "star": star,
                "count": count,
                "percent": round(percent)
            })

        return distribution

    def user_purchased_product(self):
        if not self.request.user.is_authenticated:
            return False

        return OrderItem.objects.filter(
            order__user=self.request.user,
            product=self.product
        ).exists()

    def build_context(self):
        current_qty = self.get_cart_quantity()
        reviews_page_obj, reviews_count = self.get_reviews_page()

        stock_info = self.get_stock_info()

        context = {
            "product": self.product,
            "breadcrumbs": self.get_breadcrumbs(),
            "form": AddToCartDetailForm(
                product_id=self.product.id,
                product=self.product,
                current_qty=current_qty,
            ),
            "buy_now": BuyNowForm(pk=self.product.id, quantity=current_qty or 1),
            "images": self.product.images.all(),
            "primary_image": self.product.image_url,
            "stock_label": stock_info["label"],
            "stock_icon": stock_info["icon"],
            "specs": self.product.specification.all(),
            "related": self.get_related_products(),
            "overall_rating": self.product.overall_rating,
            "reviews_page_obj": reviews_page_obj,
            "next_reviews_page": reviews_page_obj.next_page_number() if reviews_page_obj.has_next() else None,
            "reviews_count": reviews_count,
            "review_form": self.get_review_form(),
            "can_review": self.user_purchased_product() and not self.get_user_review(),
            "get_user_review": self.get_user_review(),
            "product_ratings": reviews_count,
            "rating_distribution": self.get_rating_distribution()
        }
        return context
