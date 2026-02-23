from django.db.models import Q

from ..constants import PaymentMethod, PaymentStatus
from django.db import models, transaction

from ..constants.payment import CardTypes
from ...users.models import CustomUser


class Payment(models.Model):
    payment_method = models.PositiveSmallIntegerField(
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        choices=PaymentStatus.choices
    )

    card = models.ForeignKey(
        "PaymentMethods",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    @property
    def method_label(self):
        return self.get_payment_method_display()

    @property
    def status_label(self):
        return self.get_status_display()

    @property
    def is_card(self):
        return self.payment_method == PaymentMethod.CARD

    @property
    def card_brand(self):
        if self.is_card and self.card:
            return self.card.get_card_type_display()
        return None


class PaymentMethods(models.Model):
    token = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_4 = models.CharField(max_length=4)
    name_on_card = models.CharField(max_length=50)
    expire_month = models.PositiveSmallIntegerField()
    expire_year = models.PositiveSmallIntegerField()
    card_type = models.PositiveSmallIntegerField(choices=CardTypes.choices)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(is_default=True),
                name="unique_default_card_per_user"
            )
        ]

    def __str__(self):
        return f"{self.get_card_type_display()}"

    @property
    def month_year(self):
        return f"{self.expire_month:02d}/{self.expire_year}"

    def set_as_default(self):
        with transaction.atomic():
            PaymentMethods.objects.filter(user=self.user).update(is_default=False)

            PaymentMethods.objects.filter(pk=self.pk).update(is_default=True)

            self.refresh_from_db()
