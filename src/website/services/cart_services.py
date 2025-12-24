from decimal import Decimal

from django.shortcuts import get_object_or_404

from src.core.models import Product
from src.website.forms.cart import (
    RemoveFromCartForm,
    UpdateCart,
    DropCart,
    CheckoutForm,
    PromoForm,
)
from src.website.services import Cart


class CartServiceResult:
    def __init__(self, success, quantity=None, max_available=None, error=None):
        self.success = success
        self.quantity = quantity
        self.max_available = max_available
        self.error = error

    @staticmethod
    def ok(quantity=None, quantity_in_cart=None, max_available=None):
        return CartServiceResult(
            success=True,
            quantity=quantity_in_cart or quantity,
            max_available=max_available,
        )

    @staticmethod
    def fail(error, max_available=None, quantity_in_cart=None):
        return CartServiceResult(False, error=error, max_available=max_available)


class CartService:
    def __init__(self, request):
        self.request = request
        self.cart = Cart(request)

    def _apply_stock_limit(self, product, requested_qty):
        if requested_qty < 1:
            return 1
        return min(requested_qty, product.quantity)

    def _check_stock(self, product, requested_qty):
        if requested_qty <= 0:
            return False, 0
        if requested_qty > product.quantity:
            return False, product.quantity
        return True, product.quantity

    def add_product(self, product_id, quantity):
        product = get_object_or_404(Product, pk=product_id)
        product_id = str(product_id)
        stock_available = product.quantity
        existing_qty = self.cart.cart.get(product_id, {}).get("quantity", 0)

        remaining_capacity = stock_available - existing_qty
        if remaining_capacity <= 0:
            return CartServiceResult.fail(
                "out_of_stock",
                quantity_in_cart=existing_qty,
                max_available=stock_available
            )

        qty_to_add = min(quantity, remaining_capacity)

        if product_id in self.cart.cart:
            self.cart.cart[product_id]["quantity"] = existing_qty + qty_to_add
        else:
            self.cart.cart[product_id] = {
                "id": product_id,
                "name": product.name,
                "price": float(product.price),
                "quantity": qty_to_add,
                "subcategory": product.subcategory_id,
            }

        self.cart.save()
        return CartServiceResult.ok(
            quantity_in_cart=existing_qty + qty_to_add,
            max_available=stock_available
        )

    def update_quantity(self, product_id, quantity):
        product = get_object_or_404(Product, pk=product_id)
        product_id = str(product_id)

        quantity = max(1, quantity)
        quantity = min(quantity, product.quantity)

        if product_id in self.cart.cart:
            self.cart.cart[product_id]["quantity"] = quantity
            self.cart.save()
            return CartServiceResult.ok(quantity_in_cart=quantity, max_available=product.quantity)

        return CartServiceResult.fail("not_in_cart")

    def check_stock_before_increment(self, product_id, requested_qty):
        product = get_object_or_404(Product, pk=product_id)
        max_available = product.quantity

        requested_qty = max(1, requested_qty)

        if requested_qty > max_available:
            return CartServiceResult.fail(
                error="out_of_stock", max_available=max_available
            )

        return CartServiceResult.ok(max_available=max_available)

    def remove_product(self, product_id):
        if str(product_id) in self.cart.cart:
            self.cart.remove(product_id)
            return CartServiceResult.ok()
        return CartServiceResult.fail("not_in_cart")

    def clear_cart(self):
        self.cart.clear()
        return CartServiceResult.ok()

    def get_cart_context(self):
        cart_items = []
        total_quantity = 0
        total_price = Decimal("0.00")

        for product_id, item in self.cart.cart.items():
            product = get_object_or_404(Product, pk=product_id)
            quantity = item["quantity"]
            price = item.get("price", product.price)
            subtotal = Decimal(price) * quantity
            total_quantity += quantity
            total_price += subtotal

            cart_items.append({
                "id": product_id,
                "name": product.name,
                "price": Decimal(price).quantize(Decimal(".00")),
                "quantity": quantity,
                "image": product.image,
                "description": product.description,
                "subcategory": product.subcategory,
                "remove_form": RemoveFromCartForm(product_id=product_id),
                "update_form": UpdateCart(product_id=product_id, quantity=quantity),
                "subtotal": subtotal,
                "stock": "In Stock" if product.quantity >= 10 else "Low Stock",
            })

        subtotal_decimal = total_price.quantize(Decimal(".00"))
        tax_rate = Decimal("0.08")
        tax = subtotal_decimal * tax_rate
        grand_total = subtotal_decimal + tax

        return {
            "cart_items": cart_items,
            "cart_count": total_quantity,
            "num_items": "item" if total_quantity == 1 else "items",
            "total": subtotal_decimal,
            "tax": round(tax, 2),
            "grand_total": round(grand_total, 2),
            "shipping": "FREE" if subtotal_decimal > 50 else "Standard charge",
            "drop_form": DropCart(),
            "checkout_form": CheckoutForm(),
            "promo_form": PromoForm(),
        }
