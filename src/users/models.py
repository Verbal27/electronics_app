from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    password = models.CharField(max_length=16, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.email
