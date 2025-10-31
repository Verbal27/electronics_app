from django.db import models
from django.urls import reverse
from ..users.models import CustomUser
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=50, null=False)
    category_id = models.ForeignKey(
        Category, verbose_name=("Category"), on_delete=models.CASCADE, null=False
    )

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategorys"

    def __str__(self):
        return self.subcategory_name

    def get_absolute_url(self):
        return reverse("Subcategory_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=False)
    subcategory_id = models.ForeignKey(
        Subcategory, verbose_name=("Subcategory"), on_delete=models.CASCADE, null=False
    )
    stock = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.CharField(max_length=500, null=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class Payment(models.Model):
    METHOD = [("C", "Card"), ("T", "Transfer"), ("CH", "Cash")]

    STATUS = [("P", "Pending"), ("F", "Failed"), ("C", "Completed"), ("R", "Refunded")]

    user_id = models.IntegerField(null=False)
    payment_method = models.CharField(max_length=20, choices=METHOD)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS)
    order_id = models.IntegerField(null=False)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def get_absolute_url(self):
        return reverse("Payment_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    STATUS = [
        ("P", "Pending"),
        ("C", "Completed"),
        ("CA", "Cancelled"),
        ("R", "Returned"),
    ]

    user_id = models.ForeignKey(
        CustomUser, related_name="User", on_delete=models.CASCADE, null=False
    )
    date_created = models.DateField(default=date.today)
    address = models.CharField(max_length=150, blank=False, null=False)
    payment_id = models.OneToOneField(
        Payment, verbose_name="Payment", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})


class ItemOrdered(models.Model):
    product_name = models.CharField(max_length=100, null=False)
    product_id = models.ForeignKey(
        Product, verbose_name="Product", on_delete=models.CASCADE, null=False
    )
    quantity = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    order_id = models.ForeignKey(
        Order, verbose_name="Order", on_delete=models.CASCADE, null=False
    )

    class Meta:
        verbose_name = "ItemOrdered"
        verbose_name_plural = "ItemOrdereds"

    def __str__(self) -> str:
        return self.product_name
