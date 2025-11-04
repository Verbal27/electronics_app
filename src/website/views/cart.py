from django.shortcuts import render, redirect, get_object_or_404
from ..services import Cart
from src.core.models import Product
from django.views.generic import ListView


class CartListView(ListView):
    def cart_view(self, request):
        self.cart = Cart(request)
        cart_items_with_products = []
        for pid, item in self.cart.cart.items():
            product = Product.objects.get(pk=pid)
            cart_items_with_products.append(
                {
                    "id": pid,
                    "name": item["name"],
                    "price": item["price"],
                    "quantity": item["quantity"],
                    "image": product.image,
                    "description": product.description,
                }
            )

        context = {
            "cart_items": cart_items_with_products,
            "total": self.cart.get_total(),
        }
        return render(request, "cart.html", context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.add(product_id, product.name, float(product.price), quantity=1)
    return redirect("homepage")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart")


def update_cart(request, product_id):
    quantity = int(request.POST.get("quantity", 1))
    cart = Cart(request)
    cart.update(product_id, quantity)
    return redirect("cart")


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("homepage")
