from django.db.models import IntegerChoices


class PaymentMethod(IntegerChoices):
    CARD = 1, "Cash"
    CASH = 2, "Card"


class PaymentStatus(IntegerChoices):
    PENDING = 1, "Pending"
    FAILED = 2, "Failed"
    COMPLETED = 3, "Completed"
    REFUNDED = 4, "Refunded"
