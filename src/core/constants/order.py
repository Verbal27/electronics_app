from django.db.models import IntegerChoices


class OrderStatus(IntegerChoices):
    PENDING = 1, "Pending"
    COMPLETED = 2, "Completed"
    CANCELLED = 3, "Cancelled"
    RETURNED = 4, "Returned"
