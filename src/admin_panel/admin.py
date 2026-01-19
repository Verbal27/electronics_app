from django.contrib import admin
from ..core.models import ShippingOption


@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ("code", "price", "is_active")
