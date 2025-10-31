from django.db.models import IntegerChoices


class PaymentMethod(IntegerChoices):
    CARD = 1, "Card"
    TRANSFER = 2, "Transfer"
    CASH = 3, "Cash"


class PaymentStatus(IntegerChoices):
    PENDING = 1, "Pending"
    FAILED = 2, "Failed"
    COMPLETED = 3, "Completed"
    REFUNDED = 4, "Refunded"
