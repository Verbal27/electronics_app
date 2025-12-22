import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from src.website.services.cart_services import CartService


class CartListView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CartService(self.request)
        cart_context = service.get_cart_context()
        context.update(cart_context)
        return context


class CartAddView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get("quantity", 1))
        service = CartService(request)
        result = service.add_product(product_id, quantity)

        if result.success:
            messages.success(request, "Product added successfully.")
            return redirect("homepage")
        else:
            messages.error(request, f"Cannot add product. Max available: {result.max_available}")
            return redirect("product_detail", pk=product_id)


class CartRemoveItemView(View):
    def post(self, request, product_id):
        service = CartService(request)
        result = service.remove_product(product_id)

        if result.success:
            messages.success(request, "Product removed successfully.")
        else:
            messages.error(request, "Something went wrong.")
        return redirect("cart")


class CartUpdateQuantityView(View):
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            quantity = int(data.get("quantity", 1))
        except (TypeError, ValueError, json.JSONDecodeError):
            return JsonResponse({"success": False, "error": "invalid_quantity"}, status=400)

        service = CartService(request)
        result = service.update_quantity(product_id, quantity)

        if result.success:
            return JsonResponse({"success": True, "quantity": result.quantity, "status": 200})
        else:
            return JsonResponse({
                "success": False,
                "error": result.error,
                "max_available": result.max_available,
                "status": 400
            })


class CartDropView(View):
    def post(self, request):
        service = CartService(request)
        result = service.clear_cart()

        if result.success:
            return JsonResponse({"success": True, "status": 200})
        else:
            return JsonResponse({"success": False, "error": result.error, "status": 400})
