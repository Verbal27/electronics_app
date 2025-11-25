from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.email
