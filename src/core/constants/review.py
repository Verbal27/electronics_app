from django.db.models import IntegerChoices


class ModerationStatus(IntegerChoices):
    PENDING = 1, "Pending"
    APPROVED = 2, "Approved"
    REJECTED = 3, "Rejected"
    FLAGGED = 4, "Flagged"
