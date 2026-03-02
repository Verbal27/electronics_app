from django.contrib.auth.models import AbstractUser
from django.db import models

from electronics_app.settings import PROFILE_IMAGE_PLACEHOLDER


def user_profile_upload_path(obj, filename):
    if obj.pk:
        return f"users/{obj.pk}/profile/{filename}"
    return f"users/temp/{filename}"


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date_joined = models.DateField(auto_now_add=True)
    profile_image = models.ImageField(
        upload_to=user_profile_upload_path,
        blank=True,
        null=True
    )
    order_updates = models.BooleanField(default=True)
    promo_emails = models.BooleanField(default=False)
    product_recommendations = models.BooleanField(default=False)
    two_factor_auth = models.BooleanField(default=False)
    last_password_change = models.DateField(null=True)

    def __str__(self):
        return self.email

    @property
    def has_profile_image(self):
        if self.profile_image and self.profile_image.storage.exists(self.profile_image.name):
            return True
        return False

    @property
    def profile_image_url(self):
        if self.profile_image and self.has_profile_image:
            return self.profile_image.url
        return PROFILE_IMAGE_PLACEHOLDER

    @property
    def month_year_joined(self):
        return self.date_joined.strftime('%B %Y')
