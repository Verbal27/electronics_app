import logging
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from src.website.services.cart_services import CartService


logger = logging.getLogger(__name__)


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

        if result["success"]:
            messages.success(request, "Product added successfully.")
            return redirect("homepage")
        else:
            messages.error(request, f"Cannot add product. Max available: {result["max_available"]}")
            return redirect("product_detail", pk=product_id)


class CartRemoveItemView(View):
    def post(self, request, product_id):
        service = CartService(request)
        result = service.remove_product(product_id)

        if result["success"]:
            messages.success(request, "Product removed successfully.")
        else:
            messages.error(request, "Something went wrong.")
        return redirect("cart")


class CartUpdateIncreaseQuantityView(View):
    def post(self, request, product_id):
        try:
            service = CartService(request)
            result = service.increase_quantity(product_id)
            context = service.get_cart_context()
            if result["success"]:
                return JsonResponse(
                    {
                        "success": True,
                        "quantity": result["quantity"],
                        "new_subtotal": str(result["new_subtotal"]),
                        "cart_total": str(context["total"]),
                        "tax": str(context["tax"]),
                        "grand_total": str(context["grand_total"]),
                        "has_more": result["has_more"],
                    },
                    status=200,
                )
            else:
                return JsonResponse({"success": False, "message": "Something went wrong."}, status=400)
        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class CartUpdateDecreaseQuantityView(View):
    def post(self, request, product_id):
        try:
            service = CartService(request)
            result = service.decrease_quantity(product_id)
            context = service.get_cart_context()

            if result["success"]:
                return JsonResponse(
                    {
                        "success": True,
                        "quantity": result["quantity"],
                        "new_subtotal": str(result["new_subtotal"]),
                        "cart_total": str(context["total"]),
                        "tax": str(context["tax"]),
                        "grand_total": str(context["grand_total"]),
                        "has_more": result["has_more"],
                    },
                    status=200,
                )
            else:
                return JsonResponse({"success": False, "message": "Something went wrong."}, status=400)
        except Exception as e:
            logger.error(e)
            return JsonResponse(
                {
                    "success": False,
                }
            )


class CartDropView(View):
    def post(self, request):
        service = CartService(request)
        result = service.clear_cart()

        if result.success:
            return JsonResponse({"success": True, "status": 200})
        else:
            return JsonResponse({"success": False, "error": result.error, "status": 400})
