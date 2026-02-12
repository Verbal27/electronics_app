from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=120,
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_products", args=[self.pk])
