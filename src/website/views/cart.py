from decimal import Decimal

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View

from src.core.models import Product, Subcategory
from src.core.utils.subcategory_list import list_subcategories
from src.website.forms.cart import (
    RemoveFromCartForm,
    UpdateCart,
    DropCart,
    CheckoutForm,
    PromoForm,
)
from src.website.services import Cart
from src.core.utils.availability_check import check_stock


class CartListView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)

        product_ids = cart.cart.keys()

        if product_ids:
            products = Product.objects.filter(pk__in=product_ids)
            products_map = {str(p.pk): p for p in products}
            cart_items_with_products = []

            for id, item in cart.cart.items():
                product = products_map.get(id)

                if not product:
                    continue

                sub = Subcategory.objects.get(pk=item["subcategory"])

                cart_items_with_products.append(
                    {
                        "id": id,
                        "name": item["name"],
                        "price": item["price"],
                        "quantity": item["quantity"],
                        "image": product.image,
                        "description": product.description,
                        "subcategory": sub,
                        "remove_form": RemoveFromCartForm(product_id=id),
                        "update_form": UpdateCart(
                            product_id=id, quantity=item["quantity"]
                        ),
                    }
                )
            context["cart_items"] = cart_items_with_products
            context["promo_form"] = PromoForm()
            count = 0
            for item in cart_items_with_products:
                item["price"] = Decimal(item["price"]).quantize(Decimal(".00"))
                quantity = item["quantity"] - 1
                count += 1
                count = count+quantity
                item["subtotal"] = item["price"] * item["quantity"]
                product = Product.objects.get(pk=item["id"])
                if product.quantity >= 10:
                    item["stock"] = "In Stock"
                if product.quantity < 10:
                    item["stock"] = "Low Stock"
            context["cart_count"] = count
            if count == 1:
                num_items = "item"
            else:
                num_items = "items"
            context["num_items"] = num_items
            context["drop_form"] = DropCart()
            context["checkout_form"] = CheckoutForm()
            context["total"] = cart.get_total()
            if context["total"] > 50:
                context["shipping"] = "FREE"
            else:
                context["shipping"] = "Standard charge"

            subtotal = Decimal(context["total"]).quantize(Decimal(".00"))
            tax_rate = 0.08
            tax = subtotal * Decimal(tax_rate)
            grand_total = subtotal + tax

            context["tax"] = round(tax, 2)
            context["grand_total"] = round(grand_total, 2)
        else:
            context["subcategories"] = list_subcategories(self.request)[:4]
        return context


class CartAddView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        product: Product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get("quantity", 1))
        if not check_stock(request, product, quantity, mode="add"):
            return redirect("product_detail", pk=product_id)
        try:
            cart.add(
                product_id=product.pk,
                name=product.name,
                price=float(product.price),
                quantity=quantity,
                subcategory=product.subcategory_id,
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
        product: Product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get("quantity", 1))
        if not check_stock(request, product, quantity, mode="update"):
            return redirect("cart")
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
        cart.clear()
        messages.success(request, "Cart cleared!")
        return redirect("homepage")
