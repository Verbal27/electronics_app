from django.db import models
from .subcategory import Subcategory


class Product(models.Model):
    name = models.CharField(max_length=150)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
