from django.contrib import messages


def check_stock(request, product, quantity, mode="add"):
    cart = request.session.get("cart", {})
    product_id = str(product.pk)

    existing_qty = cart.get(product_id, {}).get("quantity", 0)

    if mode == "add":
        total_requested = existing_qty + quantity
    elif mode == "update":
        total_requested = quantity
    else:
        total_requested = quantity

    if total_requested > product.quantity:
        messages.error(
            request,
            f"Not enough stock. "
            f"Requested: {total_requested}, "
            f"available: {product.quantity}."
        )
        return False

    return True
