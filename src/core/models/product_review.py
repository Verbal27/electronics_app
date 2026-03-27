from django.apps import apps
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import OuterRef, Exists
from django.utils import timezone
from django.utils.timesince import timesince

from src.core.constants import ProductReviewStatus
from src.core.models import Product
from src.users.models import CustomUser


class ProductReviewQuerySet(models.QuerySet):

    def with_verified_purchase(self):
        OrderItem = apps.get_model("core", "OrderItem")

        verified = OrderItem.objects.filter(
            order__user=OuterRef("user"),
            product=OuterRef("product"),
            order__status__in=[1, 2, 3],
        )

        return self.annotate(
            verified_purchase=Exists(verified)
        )

    def approved(self):
        return self.filter(moderation_status=ProductReviewStatus.APPROVED)


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
    )
    title = models.CharField(max_length=100)
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ProductReviewQuerySet.as_manager()
    moderation_status = models.PositiveSmallIntegerField(
        choices=ProductReviewStatus.choices,
        default=ProductReviewStatus.PENDING
    )
    moderated_at = models.DateTimeField(null=True, blank=True)
    moderated_by = models.ForeignKey(
        "users.CustomUser",
        null=True,
        blank=True,
        related_name="moderated_reviews",
        on_delete=models.SET_NULL
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_review_per_product",
            )
        ]

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
