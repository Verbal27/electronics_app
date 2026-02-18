from django.views.generic import ListView
from src.core.models.order import SavedAddress


class AddressListView(ListView):
    model = SavedAddress
    template_name = "addresses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saved_addresses = SavedAddress.objects.filter(user=self.request.user)

        context["saved_addresses"] = saved_addresses

        return context
