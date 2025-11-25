from django.db import models
from django.contrib.auth import get_user_model
from .product import Product
from .payment import Payment

from ..constants import OrderStatus

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices)
    created_at = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=15, null=True)

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
