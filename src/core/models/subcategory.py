from django.db import models
from .category import Category


class Subcategory(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.name
