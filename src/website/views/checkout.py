
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.core.models import Order
from src.website.forms.checkout import OrderModelForm
from src.website.services import Cart

class UserLoginMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

class CheckoutCreateView(CreateView):
    model = Order
    form_class = OrderModelForm
    template_name = "checkout.html"
    success_url = reverse_lazy("checkout_confirm")

    def get_form_kwargs(self):
        cart = Cart(self.request)
        kwargs = super().get_form_kwargs()
        kwargs['cart_items'] = cart.items()
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

        context["cart_items"] = cart.items()
        context["total"] = cart.get_total()

        return context