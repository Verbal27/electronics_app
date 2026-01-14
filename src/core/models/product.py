from .subcategory import Subcategory
from django.urls import reverse
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
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
