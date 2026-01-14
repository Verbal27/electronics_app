import logging
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from src.core.utils.subcategory_list import list_popular_subcategories
from src.website.services.cart_services import CartService


logger = logging.getLogger(__name__)


class CartListView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CartService(self.request)
        cart_context = service.get_cart_context()
        context.update(cart_context)

        context["subcategories"] = list_popular_subcategories(self.request)

        return context


class CartAddView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get("quantity", 1))
        service = CartService(request)
        result = service.add_product(product_id, quantity)

        data = result["data"]

        if result["success"]:
            messages.success(request, "Product added successfully.")
            return redirect("homepage")
        else:
            messages.error(request, f"Cannot add product. Max available: {data["max_available"]}")
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

            if not result["success"]:
                return JsonResponse(
                    {
                        "success": False,
                        "message": result["message"],
                        "data": {}
                    },
                    status=400,
                )

            data = result["data"]

            return JsonResponse(
                {
                    "success": True,
                    "message": "Product updated successfully",
                    "data": {
                        "quantity": data["quantity"],
                        "new_subtotal": str(data["new_subtotal"]),
                        "cart_total": str(context["total"]),
                        "tax": str(context["tax"]),
                        "grand_total": str(context["grand_total"]),
                        "has_more": data["has_more"],
                    },
                },
                status=200,
            )

        except Exception as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "success": False,
                    "message": "Internal server error",
                    "data": {}
                },
                status=500,
            )


class CartUpdateDecreaseQuantityView(View):
    def post(self, request, product_id):
        try:
            service = CartService(request)
            result = service.decrease_quantity(product_id)
            context = service.get_cart_context()

            if not result["success"]:
                return JsonResponse(
                    {
                        "success": False,
                        "message": result["message"],
                        "data": {}
                    },
                    status=400,
                )

            data = result["data"]

            return JsonResponse(
                {
                    "success": True,
                    "message": "Product updated successfully",
                    "data": {
                        "quantity": data["quantity"],
                        "new_subtotal": str(data["new_subtotal"]),
                        "cart_total": str(context["total"]),
                        "tax": str(context["tax"]),
                        "grand_total": str(context["grand_total"]),
                        "has_more": data["has_more"],
                    },
                },
                status=200,
            )

        except Exception as e:
            logger.exception(e)
            return JsonResponse(
                {
                    "success": False,
                    "message": "Internal server error",
                    "data": {}
                },
                status=500,
            )


class CartDropView(View):
    def post(self, request):
        service = CartService(request)
        result = service.clear_cart()

        if result["success"]:
            return JsonResponse(
                {
                    "success": True,
                    "message": "Cart cleared successfully",
                    "data": {}
                },
                status=200
            )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": result,
                    "data": {}
                },
                status=500
            )
