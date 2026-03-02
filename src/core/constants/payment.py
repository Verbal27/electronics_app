from django.db.models import IntegerChoices


class PaymentMethod(IntegerChoices):
    CASH = 1, "Cash"
    CARD = 2, "Card"


class PaymentStatus(IntegerChoices):
    PENDING = 1, "Pending"
    FAILED = 2, "Failed"
    COMPLETED = 3, "Completed"
    REFUNDED = 4, "Refunded"


class CardTypes(IntegerChoices):
    UNKNOWN = 0, "Unknown"
    VISA = 1, "Visa"
    MASTERCARD = 2, "Mastercard"
    AMEX = 3, "American Express"
