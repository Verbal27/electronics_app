from decimal import Decimal

from src.core.models import Product, ShippingOption
from src.website.services import CartService


class CheckoutService:
    def __init__(self, request):
        self.request = request
        self.cart_service = CartService(request)
        self.cart = self.cart_service.cart

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

    def check_and_reserve_stock(self):
        items = list(self.cart.items())

        if not items:
            return {"success": False, "message": "Your cart is empty."}

        products = {
            item["id"]: Product.objects.select_for_update().get(pk=item["id"])
            for item in items
        }

        unavailable = []

        for item in items:
            product = products[item["id"]]
            if product.quantity < item["quantity"]:
                unavailable.append(
                    f"{product.name} "
                    f"(available: {product.quantity}, requested: {item['quantity']})"
                )

        if unavailable:
            return {
                "success": False,
                "message": "Some products are unavailable.",
                "data": {"unavailable_items": unavailable},
            }

        for item in items:
            product = products[item["id"]]
            product.quantity -= item["quantity"]
            product.save(update_fields=["quantity"])

        return {"success": True}
