from django.apps import apps
from django.db import models
from django.db.models import OuterRef, Exists


class ProductReviewQuerySet(models.QuerySet):

    def with_verified_purchase(self):
        OrderItem = apps.get_model("core", "OrderItem")

        verified = OrderItem.objects.filter(
            order__user=OuterRef("user"),
            product=OuterRef("product"),
            order__status__in=[1, 2, 3],
        )

        return self.annotate(
            verified_purchase=Exists(verified)
        )
