import json
from django.http import JsonResponse
from django.views import View
from src.website.services.cart_services import CartService


class CheckStockView(View):
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            requested_qty = int(data.get("quantity", 1))
        except Exception:
            return JsonResponse({"success": False, "error": "invalid_quantity"}, status=400)

        service = CartService(request)
        result = service.check_stock_before_increment(product_id, requested_qty)

        if result.success:
            return JsonResponse({
                "success": True,
                "max_available": result.max_available
            }, status=200)

        return JsonResponse({
            "success": False,
            "error": result.error,
            "max_available": result.max_available,
        }, status=400)
