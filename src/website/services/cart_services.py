from django.shortcuts import get_object_or_404
from src.core.components.website.span import Span
from src.core.models import Product
from src.core.utils.subcategory_list import list_popular_subcategories
from src.website.forms.cart import (
    RemoveFromCartForm,
    UpdateCart,
    DropCart,
    CheckoutForm,
    PromoForm,
)
from src.website.services import Cart
from decimal import Decimal


class CartService:
    def __init__(self, request):
        self.request = request
        self.cart = Cart(request)

    def add_product(self, product_id, quantity):
        product = get_object_or_404(Product, pk=product_id)
        product_id = str(product_id)
        stock_available = product.quantity
        existing_qty = self.cart.cart.get(product_id, {}).get("quantity", 0)

        remaining_capacity = stock_available - existing_qty
        if remaining_capacity == 0:
            return {
                "success": False,
                "message": "Out of stock",
                "data": {
                    "quantity_in_cart": existing_qty,
                    "max_available": stock_available,
                },
            }

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
        return {
            "success": True,
            "message": "Added successfully",
            "data": {
                "max_available": stock_available,
                "quantity_in_cart": existing_qty + qty_to_add,
            },
        }

    def increase_quantity(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product_id = str(product_id)
        price = Decimal(product.price)

        if product_id not in self.cart.cart:
            return {
                "success": False,
                "message": "Product not in cart",
                "data": {}
            }

        current = self.cart.cart[product_id]["quantity"]

        if current == product.quantity:
            return {
                "success": True,
                "message": "Max stock reached",
                "data": {
                    "quantity": product.quantity,
                    "new_subtotal": price * product.quantity,
                    "has_more": False,
                },
            }

        new_quantity = current + 1

        subtotal = price * new_quantity
        subtotal = Decimal(subtotal)

        self.cart.cart[product_id]["quantity"] = new_quantity
        self.cart.save()

        return {
            "success": True,
            "message": "Product updated successfully",
            "data": {
                "quantity": new_quantity,
                "new_subtotal": subtotal,
                "has_more": True,
            },
        }

    def decrease_quantity(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product_id = str(product_id)
        price = Decimal(product.price)

        if product_id not in self.cart.cart:
            return {
                "success": False,
                "message": "Product not in cart",
                "data": {}
            }

        current = self.cart.cart[product_id]["quantity"]
        new_quantity = current - 1

        if current == 1:
            return {
                "success": True,
                "message": "Minimum reached",
                "data": {
                    "quantity": current,
                    "new_subtotal": price * current,
                    "has_more": current < product.quantity,
                },
            }

        new_subtotal = price * new_quantity

        self.cart.cart[product_id]["quantity"] = new_quantity
        self.cart.save()

        return {
            "success": True,
            "message": "Decreased quantity",
            "data": {
                "quantity": new_quantity,
                "new_subtotal": new_subtotal,
                "has_more": new_quantity < product.quantity,
            },
        }

    def remove_product(self, product_id):
        if str(product_id) in self.cart.cart:
            self.cart.remove(product_id)
            return {
                "success": True,
                "message": "Removed successfully",
                "data": {}
            }
        return {
            "success": False,
            "message": "Not in cart",
            "data": {}
        }

    def clear_cart(self):
        self.cart.clear()
        return {
            "success": True,
            "message": "Cleared successfully",
            "data": {}
        }

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
            stock_label_content = "Low stock" if product.quantity <= 10 else "In stock"
            stock_label_css_classes = "text-warning" if product.quantity <= 10 else "text-success"

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
                "subtotal": Decimal(subtotal).quantize(Decimal(".00")),
                "stock_label": Span(
                    content=stock_label_content,
                    title=stock_label_content,
                    css_classes=stock_label_css_classes
                ),
            })

        subtotal_decimal = total_price.quantize(Decimal(".00"))
        tax_rate = Decimal("0.08")
        tax = subtotal_decimal * tax_rate
        grand_total = subtotal_decimal + tax

        subcategories = list_popular_subcategories(self.request)

        return {
            "cart_items": cart_items,
            "cart_count": total_quantity,
            "num_items": "item" if total_quantity == 1 else "items",
            "total": Decimal(subtotal_decimal).quantize(Decimal(".00")),
            "tax": Decimal(tax).quantize(Decimal(".00")),
            "grand_total": Decimal(grand_total).quantize(Decimal(".00")),
            "shipping": "FREE" if subtotal_decimal > 50 else "Standard charge",
            "drop_form": DropCart(),
            "checkout_form": CheckoutForm(),
            "promo_form": PromoForm(),
            "subcategories": subcategories,
        }
