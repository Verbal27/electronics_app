from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.views.generic import TemplateView

from src.core.models import Order


class CabinetTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cabinet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user:
            orders = (
                Order.objects.filter(
                    user=user
                ).select_related(
                    "payment"
                ).prefetch_related(
                    "items"
                )
            )
            context["orders"] = orders
            return context
        else:
            return redirect_to_login(self.login_url)
