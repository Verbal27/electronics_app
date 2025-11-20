from decimal import Decimal

from django.db.models.functions import Round
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View
from src.core.models import Product
from django.contrib import messages

from src.website.forms import OrderModelForm
from src.website.forms.cart import (
    AddToCartForm,
    RemoveFromCartForm,
    UpdateCart,
    DropCart,
    CheckoutForm,
)
from src.website.services import Cart


class CartListView(TemplateView):
    template_name = "cart.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)

        product_ids = cart.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        products_map = {str(p.pk): p for p in products}

        cart_items_with_products = []
        for pid, item in cart.cart.items():
            product = products_map.get(pid)
            if product:
                cart_items_with_products.append(
                    {
                        "id": pid,
                        "name": item["name"],
                        "price": float(item["price"]),
                        "quantity": item["quantity"],
                        "image": product.image,
                        "description": product.description,
                        "remove_form": RemoveFromCartForm(product_id=pid),
                        "update_form": UpdateCart(product_id=pid, quantity=item["quantity"]),
                    }
                )

        context["cart_items"] = cart_items_with_products
        context["drop_form"] = DropCart()
        context["checkout_form"] = CheckoutForm()
        context["total"] = cart.get_total()
        return context


class CartAddView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        form = AddToCartForm(request.POST, product_id=product_id)
        product: Product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get("quantity", 1))
        try:
            cart.add(
                product_id=product.pk,
                name=product.name,
                price=float(product.price),
                quantity=quantity,
            )
            messages.success(request, "Product added sucessfully")
            return redirect("homepage")
        except Exception:
            messages.error(
                request, "There was a problem adding this item to your cart."
            )
            return redirect("homepage")


class CartRemoveItemView(View):
    form_class = RemoveFromCartForm

    def post(self, request, product_id):
        cart = Cart(request)
        form = RemoveFromCartForm(request.POST, product_id=product_id)
        product: Product = get_object_or_404(Product, pk=product_id)
        try:
            cart.remove(product_id=product.pk)
            messages.success(request, "Item removed successfully!")
            return redirect("cart")
        except Exception:
            messages.error(
                request, "There was a problem removing this item from your cart."
            )
            return redirect("cart")


class CartUpdateQuantityView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        form = UpdateCart(request.POST, product_id=product_id)
        product: Product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get("quantity", 1))

        try:
            cart.update(product_id=product.pk, quantity=quantity)
            messages.success(request, "Item quantity updated successfully!")
            return redirect("cart")
        except Exception:
            messages.error(
                request, "There was a problem updating this item in your cart."
            )
            return redirect("cart")


class CartDropView(View):
    form_class = DropCart

    def post(self, request):
        cart = Cart(request)
        form = self.form_class(request.POST)
        cart.clear()
        messages.success(request, "Cart cleared!")
        return redirect("homepage")
