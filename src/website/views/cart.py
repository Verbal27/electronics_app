from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View
from src.core.models import Product
from django.contrib import messages
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
                        "price": item["price"],
                        "quantity": item["quantity"],
                        "image": product.image,
                        "description": product.description,
                    }
                )

        context["cart_items"] = cart_items_with_products
        context["total"] = cart.get_total()
        return context


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product: Product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get("quantity", 1))
        try:
            cart.add(
                product_id=product.pk,
                name=product.name,
                price=float(product.price),
                quantity=quantity,
            )
        except Exception as e:
            print(f"Error adding product to cart: {e}")
            messages.error(
                request, "There was a problem adding this item to your cart."
            )
            return redirect("cart")

        return redirect("homepage")

    def get(self, request, product_id):
        return self.post(request, product_id)


class CartRemoveItemView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product: Product = get_object_or_404(Product, pk=product_id)
        try:
            cart.remove(product_id=product.pk)
        except Exception as e:
            print(f"Error removing product from cart: {e}")
            messages.error(
                request, "There was a problem removing this item from your cart."
            )
            return redirect("cart")
        return redirect("cart")

    def get(self, request, product_id):
        return self.post(request, product_id)


class CartUpdateQuantityView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product: Product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get("quantity", 1))

        try:
            cart.update(product_id=product.pk, quantity=quantity)
        except Exception as e:
            print(f"Error updating product quantity from cart: {e}")
            messages.error(
                request, "There was a problem updating this item in your cart."
            )
            return redirect("cart")
        return redirect("cart")

    def get(self, request, product_id):
        return self.post(request, product_id)


class CartDropView(View):
    def post(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect("homepage")

    def get(self, request):
        return self.post(request)
