from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView

from src.core.components.cabinet.order_card import OrderCard
from src.core.components.cabinet_context import CabinetContextMixin
from src.core.models import Order


class OrderListView(LoginRequiredMixin, CabinetContextMixin, ListView):
    model = Order
    template_name = "order/orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user, status=1)
            .select_related("payment")
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_cards = [
            OrderCard(self.request, order)
            for order in context["orders"]
        ]

        context["order_cards"] = order_cards

        return context


class OrderInfiniteScrollView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user, status=1)
            .select_related("payment", "shipping")
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    def render_to_response(self, context, **response_kwargs):
        orders = context["orders"]

        order_cards = [
            OrderCard(self.request, order)
            for order in orders
        ]

        html = render_to_string(
            "partials/order_list_items.html",
            {"order_cards": order_cards},
            request=self.request
        )

        return JsonResponse({
            "html": html,
            "has_next": context["page_obj"].has_next()
        })


class AllOrderListView(LoginRequiredMixin, CabinetContextMixin, ListView):
    model = Order
    template_name = "order/orders_all.html"
    context_object_name = "orders"
    paginate_by = 10

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


class AllOrdersInfiniteScrollView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .select_related("payment", "shipping")
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    def render_to_response(self, context, **response_kwargs):
        orders = context["orders"]

        order_cards = [
            OrderCard(self.request, order)
            for order in orders
        ]

        html = render_to_string(
            "partials/order_list_items.html",
            {"order_cards": order_cards},
            request=self.request
        )

        return JsonResponse({
            "html": html,
            "has_next": context["page_obj"].has_next()
        })


class OrderDetailView(LoginRequiredMixin, CabinetContextMixin, DetailView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .select_related("payment", "shipping")
            .prefetch_related("items__product")
        )
