from django.urls import reverse

from electronics_app.settings import SUBCATEGORY_EMPTY_CART_PLACEHOLDER_IMAGE
from .category import Category
from django.db import models


class Subcategory(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    image = models.ImageField(upload_to="subcategories/images/", null=True, blank=True)

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.name

    @property
    def has_valid_image(self):
        if self.image and self.image.storage.exists(self.image.name):
            return True
        return False

    @property
    def image_url(self):
        if self.image and self.has_valid_image:
            return self.image.url
        return SUBCATEGORY_EMPTY_CART_PLACEHOLDER_IMAGE

    def get_absolute_url(self):
        return reverse("subcategory_products", args=[self.pk])
