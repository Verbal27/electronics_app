from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from src.core.components.cabinet.order_card import OrderCard
from src.core.models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .select_related("payment")
            .prefetch_related("items__product")
            .order_by("-created_at")[:4]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_order_cards = [
            OrderCard(self.request, order)
            for order in context["orders"]
        ]

        context["order_cards"] = last_order_cards
        return context


class AllOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders_all.html"
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .select_related("payment")
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["order_cards"] = [
            OrderCard(self.request, order)
            for order in context["orders"]
        ]

        return context
