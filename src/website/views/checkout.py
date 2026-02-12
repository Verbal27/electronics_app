from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from src.core.models import ShippingOption, Order
from src.website.services import Cart, CartService, CheckoutService
from src.website.forms.checkout import OrderModelForm, BuyNowForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy


class CheckoutCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderModelForm
    template_name = "checkout.html"

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        saved_address = getattr(user, "saved_address", None)

        if saved_address:
            initial.update(
                {
                    "first_name": saved_address.first_name,
                    "last_name": saved_address.last_name,
                    "email": saved_address.email,
                    "phone": saved_address.phone,
                    "street": saved_address.street,
                    "city": saved_address.city,
                    "state": saved_address.state,
                    "zipcode": saved_address.zipcode,
                }
            )
        else:
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
        tax = (Decimal(subtotal) + Decimal(shipping_price)) * Decimal(tax_rate)
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
        if form.errors:
            messages.error(self.request, "There was an error submitting your order.")
        return super().form_invalid(form)

    def form_valid(self, form):
        checkout_service = CheckoutService(self.request)

        with transaction.atomic():
            stock_check = checkout_service.check_and_reserve_stock()
            if not stock_check["success"]:
                messages.error(self.request, stock_check["message"])
                return self.form_invalid(form)

            self.object = form.save()

        Cart(self.request).clear()
        return HttpResponseRedirect(self.get_success_url())

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

        shipping = order.shipping
        if shipping and shipping.delivery_time:
            context["delivery_time_span"] = f"{shipping.delivery_time}"
        else:
            context["delivery_time_span"] = "3–5 business days"

        return context


class BuyNowView(LoginRequiredMixin, View):
    form_class = BuyNowForm

    def post(self, request, pk):
        quantity = int(request.POST.get("quantity", 1))
        cart_service = CartService(self.request)

        cart_service.cart.clear()
        result = cart_service.add_product(pk, quantity)

        if not result["success"]:
            messages.error(request, result["message"])
            return redirect("product_detail", pk=pk)

        return redirect("checkout")
