from decimal import Decimal
from math import floor

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.utils import timezone
from django.utils.timesince import timesince

from electronics_app import settings
from electronics_app.settings import PRODUCT_PLACEHOLDER_IMAGE
from .product_review import ProductReviewQuerySet
from .subcategory import Subcategory
from django.urls import reverse
from django.db import models

from ...users.models import CustomUser


class Product(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.pk])

    @property
    def is_low_stock(self):
        if self.quantity >= 10:
            return False
        return True

    @property
    def stock_status(self):
        if self.is_low_stock:
            return "Low stock"
        return "In stock"

    @property
    def primary_image(self):
        return (
                self.images.filter(is_primary=True).first()
                or self.images.first()
        )

    @property
    def image_url(self):
        primary = self.primary_image
        if primary:
            return primary.url
        return PRODUCT_PLACEHOLDER_IMAGE

    @property
    def overall_rating(self):
        avg = self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
        return Decimal(str(avg)).quantize(Decimal(".0"))

    @property
    def product_stars(self):
        return range(floor(self.overall_rating))

    @property
    def product_empty_stars(self):
        return range(floor(5 - self.overall_rating))

    @property
    def has_half_star(self):
        rating = self.overall_rating or 0
        fraction = rating - floor(rating)
        return 0.25 <= fraction < 0.75


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_primary=True),
                name="unique_primary_image_per_product",
            )
        ]

    def __str__(self):
        return f"Image for {self.product.name}"

    @property
    def has_product_image(self):
        if self.image and self.image.storage.exists(self.image.name):
            return True
        return False

    @property
    def url(self):
        if self.image and self.has_product_image:
            return self.image.url
        return PRODUCT_PLACEHOLDER_IMAGE


class Specification(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="specification",
        on_delete=models.CASCADE,
    )
    specification_name = models.CharField(max_length=50)
    specification_value = models.CharField(max_length=50)
    specification_measurement_unit = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.specification_name}: {self.specification_value} {self.specification_measurement_unit}"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    title = models.CharField(max_length=100)
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ProductReviewQuerySet.as_manager()

    def __str__(self):
        return f"{self.user.first_name}{self.user.last_name} - {self.product.name} ({self.rating}/5)"

    @property
    def time_since(self):
        return timesince(self.created_at, timezone.now())

    @property
    def stars(self):
        return range(self.rating)

    @property
    def empty_stars(self):
        return range(5 - self.rating)

    @classmethod
    def check_cooldown(cls, user, product):
        last_review = (
            cls.objects
            .filter(user=user, product=product)
            .order_by("-created_at")
            .first()
        )

        if not last_review:
            return

        cooldown_until = last_review.created_at + settings.REVIEW_COOLDOWN

        if timezone.now() < cooldown_until:
            remaining = cooldown_until - timezone.now()
            raise ValidationError(
                f"You can review again in {remaining.seconds // 60} minutes."
            )
