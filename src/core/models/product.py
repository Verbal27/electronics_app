from electronics_app.settings import PRODUCT_PLACEHOLDER_IMAGE
from .subcategory import Subcategory
from django.urls import reverse
from django.db import models


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
    specification_name = models.CharField(max_length=50, unique=True)
    specification_value = models.CharField(max_length=50)
    specification_measurement_unit = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.specification_name}: {self.specification_value} {self.specification_measurement_unit}"
