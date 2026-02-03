from django.core.files.storage import default_storage
from django.urls import reverse

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
        return bool(
            self.image and self.image.name and default_storage.exists(self.image.name)
        )

    def get_absolute_url(self):
        return reverse("subcategory_products", args=[self.pk])

    def get_breadcrumb(self):
        return [
            {"label": "Home", "url": reverse("homepage")},
            {
                "label": self.category.name,
                "url": self.category.get_absolute_url(),
            },
            {"label": self.name, "url": self.get_absolute_url()},
        ]
