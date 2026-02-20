from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, UpdateView

from src.core.components.cabinet_context import CabinetContextMixin
from src.core.models.order import SavedAddress
from src.users.forms.addresses import ChangeSavedAddress, RemoveSavedAddressForm


class AddressListView(LoginRequiredMixin, CabinetContextMixin, ListView):
    model = SavedAddress
    template_name = "addresses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saved_addresses = SavedAddress.objects.filter(user=self.request.user)
        if saved_addresses:
            for addr in saved_addresses:
                context["delete_address"] = RemoveSavedAddressForm(pk=addr.id)

        context["saved_addresses"] = saved_addresses

        return context


class ChangeSavedAddressView(LoginRequiredMixin, CabinetContextMixin, UpdateView):
    model = SavedAddress
    form_class = ChangeSavedAddress
    template_name = "address_update.html"
    success_url = reverse_lazy("addresses")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.helper.form_action = reverse("address-update", kwargs={"pk": self.object.pk})
        return form

    def get_queryset(self):
        return SavedAddress.objects.filter(user=self.request.user)

    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)

        messages.success(self.request, "Address updated successfully")
        return response

    def form_invalid(self, form):
        if form.errors:
            messages.error(self.request, "There was an error.")
        return super().form_invalid(form)


class DeleteAddressView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(SavedAddress, pk=pk, user=request.user)
        address.delete()
        messages.success(request, "Address deleted successfully")
        return redirect("addresses")
