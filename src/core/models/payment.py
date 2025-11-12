from django.db import models
from ..constants import PaymentMethod, PaymentStatus


class Payment(models.Model):
    payment_method = models.PositiveSmallIntegerField(choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=PaymentStatus.choices)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
