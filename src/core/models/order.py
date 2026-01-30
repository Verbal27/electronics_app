from django.contrib.auth import get_user_model
from django.db import models
from .product import Product
from .payment import Payment
from ..constants import OrderStatus

User = get_user_model()


class ShippingOption(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_time = models.CharField(max_length=50, help_text="e.g. '1–2 business days', '3–5 days', 'Same day'")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Shipping option"
        verbose_name_plural = "Shipping options"

    def __str__(self):
        return f"{self.name} {self.delivery_time} {self.price}"


class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15, null=True)
    save_address = models.BooleanField(default=False)
    shipping = models.ForeignKey(
        ShippingOption,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    product_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItem"

    def __str__(self) -> str:
        return f"Order - {self.order.id} {self.product_name}"  # type: ignore


class SavedAddress(models.Model):
    user = models.OneToOneField(User, related_name="saved_address", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
