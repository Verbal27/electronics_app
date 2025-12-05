from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from src.core.models import Order


class CabinetTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cabinet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["orders"] = (
            Order.objects.filter(user=self.request.user)
            .select_related("payment")
            .prefetch_related("items")
            .order_by("-created_at")
        )

        return context
