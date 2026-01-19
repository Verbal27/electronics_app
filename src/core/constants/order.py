from django.db.models import IntegerChoices


class OrderStatus(IntegerChoices):
    PENDING = 1, "Pending"
    COMPLETED = 2, "Completed"
    CANCELLED = 3, "Cancelled"
    RETURNED = 4, "Returned"


class ShippingMethod(IntegerChoices):
    STANDARD = 1, "Standard shipping"
    EXPRESS = 2, "Express shipping"
    OVERNIGHT = 3, "Overnight shipping"
