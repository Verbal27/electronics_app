from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from src.website.services import Cart, CartService, CheckoutService
from src.website.forms.checkout import OrderModelForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


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
        checkout_service = CheckoutService(self.request)
        res = checkout_service.process_checkout(form)

        if res["success"]:
            messages.success(self.request, res.get("message"))
            return HttpResponseRedirect(self.get_success_url())

        messages.error(
            self.request,
            res.get("message", "There was an error processing your request."),
        )
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CartService(self.request)
        cart_context = service.get_cart_context()
        context.update(cart_context)

        return context
