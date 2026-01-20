from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from src.core.models import ShippingOption, Order
from src.website.services import Cart, CartService, CheckoutService
from src.website.forms.checkout import OrderModelForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy


class CheckoutCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderModelForm
    template_name = "checkout.html"

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

        subtotal = cart.get_total()
        default_shipping = ShippingOption.objects.filter(is_active=True).first()
        shipping_price = getattr(default_shipping, "price", 0)

        tax_rate = 0.08
        tax = subtotal * Decimal(tax_rate)
        grand_total = Decimal(subtotal) + Decimal(shipping_price) + tax

        kwargs.update(
            {
                "cart_items": cart.items(),
                "total": subtotal,
                "grand_total": grand_total,
                "tax": tax,
                "user": self.request.user,
            }
        )
        return kwargs

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return super().form_invalid(form)

    def form_valid(self, form):
        checkout_service = CheckoutService(self.request)
        res = checkout_service.process_checkout(form)

        if res["success"]:
            self.object = res["data"]["order"]
            return HttpResponseRedirect(self.get_success_url())

        messages.error(
            self.request,
            res.get("message", "There was an error processing your request."),
        )
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("complete", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_service = CartService(self.request)
        cart_context = cart_service.get_cart_context()
        context.update(cart_context)
        checkout_service = CheckoutService(self.request)
        initial_data = checkout_service.get_initial_data(context)

        context.update(initial_data)

        return context


class CheckoutCompleteView(LoginRequiredMixin, TemplateView):
    template_name = "checkout_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order = get_object_or_404(Order, pk=self.kwargs["pk"], user=self.request.user)

        context["order"] = order

        shipping = ShippingOption.objects.filter(code=order.shipping).first()
        if shipping and shipping.delivery_time:
            context["delivery_time_span"] = f"{shipping.delivery_time}"
        else:
            context["delivery_time_span"] = "3–5 business days"

        return context
