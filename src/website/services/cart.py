from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def add(self, product_id, name, price, quantity):
        product_id = str(product_id)
        price = str(price)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id] = {
                "pid": product_id,
                "name": name,
                "price": price,
                "quantity": quantity,
            }
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.cart = {}
        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity
            self.save()

    def get_total(self):
        total = Decimal(
            sum(Decimal(item["price"]) * Decimal(item["quantity"]) for item in self.cart.values())
        )
        return total.quantize(Decimal(".01"))

    def items(self):
        return self.cart.values()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
