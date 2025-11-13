
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.website.forms.checkout import OrderModelForm
from src.website.services import Cart


class CheckoutCreateView(LoginRequiredMixin,CreateView):
    form_class = OrderModelForm
    template_name = "checkout.html"
    success_url = reverse_lazy("checkout_confirm")

    def get_initial(self):
        user = self.request.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

    def get_form_kwargs(self):
        cart = Cart(self.request)
        kwargs = super().get_form_kwargs()
        kwargs['cart_items'] = cart.items()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        cart = Cart(self.request)
        response = super().form_valid(form)
        cart.clear()
        messages.success(self.request, "Your order has been placed.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        user = self.request.user

        context["cart_items"] = cart.items()
        context["total"] = cart.get_total()
        context["user"] = user

        return context