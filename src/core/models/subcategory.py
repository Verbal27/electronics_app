from django.core.files.storage import default_storage

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
