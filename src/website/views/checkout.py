from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.core.models import Product
from src.core.utils.availability_check import check_stock
from src.website.forms.checkout import OrderModelForm
from src.website.services import Cart


class CheckoutCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderModelForm
    template_name = "checkout.html"
    success_url = reverse_lazy("homepage")

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial.update(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        )
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cart = Cart(self.request)
        kwargs.update(
            {
                "cart_items": cart.items(),
                "total": cart.get_total(),
                "user": self.request.user,
            }
        )
        return kwargs

    def form_valid(self, form):
        cart = Cart(self.request)
        products = {
            item["id"]: Product.objects.get(pk=item["id"]) for item in cart.items()
        }

        for item in cart.items():
            product = products[item["id"]]
            if not check_stock(self.request, product, item["quantity"], mode="update"):
                return self.form_invalid(form)

        for item in cart.items():
            product = products[item["id"]]
            product.quantity -= item["quantity"]
            product.save()

        response = super().form_valid(form)
        cart.clear()
        messages.success(self.request, "Your order has been placed.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)

        context["cart_items"] = cart.items()
        context["total"] = cart.get_total()

        return context
