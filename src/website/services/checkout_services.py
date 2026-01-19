from django.db import transaction

from src.core.models import Product
from src.website.services import Cart, CartService


class CheckoutService:
    def __init__(self, request):
        self.request = request
        self.cart = Cart(request)
        self.cart_service = CartService(request)

    # def get_checkout_context(self, **kwargs):
    #     cart_items = []
    #
    #     for item in self.cart.items():
    #         product = get_object_or_404(Product, pk=item["id"])
    #         quantity = item["quantity"]
    #         price = item.get("price", product.price)
    #         cart_items.append({
    #             "id": item["id"],
    #             "name": product.name,
    #             "price": Decimal(price).quantize(Decimal(".00")),
    #             "quantity": quantity,
    #             "image": product.image,
    #         })
    #
    #     return {"cart_items": cart_items, "total": self.cart.get_total()}

    def validate_cart(self):
        unavailable_items = []
        products = {
            item["id"]: Product.objects.get(pk=item["id"]) for item in self.cart.items()
        }

        for item in self.cart.items():
            product = products[item["id"]]
            if not self.cart_service.check_available(product, product_id=product.id):
                unavailable_items.append(product.name)
        return unavailable_items

    def process_checkout(self, form):
        unavailable_items = self.validate_cart()
        if unavailable_items:
            return {
                "success": False,
                "message": "Some products are unavailable in the quantity you requested",
                "data": {"unavailable_items": unavailable_items},
            }

        with transaction.atomic():
            for item in self.cart.items():
                product = Product.objects.select_for_update().get(pk=item["id"])
                product.quantity -= item["quantity"]
                product.save()

            order = form.save(commit=True)

        self.cart.clear()
        return {
            "success": True,
            "message": "Checkout completed successfully",
            "data": {"order_id": order.id},
        }
