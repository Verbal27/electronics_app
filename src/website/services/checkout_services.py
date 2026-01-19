from decimal import Decimal

from django.db import transaction

from src.core.models import Product, ShippingOption
from src.website.services import Cart, CartService


class CheckoutService:
    def __init__(self, request):
        self.request = request
        self.cart = Cart(request)
        self.cart_service = CartService(request)

    def get_initial_data(self, context):
        form = context.get("form")

        shipping_instance = form.initial.get("shipping") if form else None

        if shipping_instance:
            context["shipping_price"] = shipping_instance.price
        else:
            default_shipping = ShippingOption.objects.filter(is_active=True).first()
            context["shipping_price"] = (
                default_shipping.price if default_shipping else 0
            )

        subtotal = context.get("total", 0)
        context["grand_total"] = Decimal(subtotal) + Decimal(
            context["shipping_price"] + Decimal(context["tax"])
        )

        return context

    def process_checkout(self, form):
        items = list(self.cart.items())

        if not items:
            return {
                "success": False,
                "message": "Your cart is empty.",
            }

        with transaction.atomic():
            products = {
                item["id"]: Product.objects.select_for_update().get(pk=item["id"])
                for item in self.cart.items()
            }

            unavailable = []
            for item in self.cart.items():
                product = products[item["id"]]
                requested_qty = item["quantity"]

                if product.quantity < requested_qty:
                    unavailable.append(
                        f"{product.name} (available: {product.quantity}, requested: {requested_qty})"
                    )

            if unavailable:
                return {
                    "success": False,
                    "message": "Some products are unavailable in the quantity you requested.",
                    "data": {"unavailable_items": unavailable},
                }

            for item in self.cart.items():
                product = products[item["id"]]
                product.quantity -= item["quantity"]
                product.save(update_fields=["quantity"])
            order = form.save(commit=True)

        self.cart.clear()

        return {
            "success": True,
            "message": "Checkout completed successfully.",
            "data": {"order": order},
        }
