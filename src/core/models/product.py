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
    def stock_status(self):
        if self.quantity >= 10:
            return "In Stock"
        return "Low Stock"

    @property
    def primary_image(self):
        return (
                self.images.filter(is_primary=True).first()
                or self.images.first()
        )

    def get_breadcrumb(self):
        return [
            {"label": "Home", "url": reverse("homepage")},
            {
                "label": self.subcategory.category.name,
                "url": self.subcategory.category.get_absolute_url(),
            },
            {"label": self.name, "url": self.get_absolute_url()},
        ]


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
    def url(self):
        return self.image.url


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
