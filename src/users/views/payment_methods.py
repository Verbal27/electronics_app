from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, View, CreateView, UpdateView

from src.core.components.cabinet_context import CabinetContextMixin
from src.core.models import PaymentMethods
from src.users.forms import (
    RemoveSavedMethodForm,
    AddNewMethod,
    SetDefaultPaymentForm,
    ChangeSavedMethod
)


class AddPaymentView(LoginRequiredMixin, CabinetContextMixin, CreateView):
    model = PaymentMethods
    template_name = "payment_methods/new_payment_method.html"
    form_class = AddNewMethod
    success_url = reverse_lazy("payment-methods")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Card added successfully!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "There was a problem adding new card")
        return super().form_invalid(form)


class SetDefaultCardView(LoginRequiredMixin, View):

    def post(self, request, pk):
        card = get_object_or_404(
            PaymentMethods,
            pk=pk,
            user=request.user
        )

        card.set_as_default()

        messages.success(request, "Default card updated.")
        return redirect("payment-methods")


class PaymentListView(LoginRequiredMixin, CabinetContextMixin, ListView):
    model = PaymentMethods
    template_name = "payment_methods/payment_methods.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        saved_methods = self.model.objects.filter(user=self.request.user)

        methods_with_forms = []
        for method in saved_methods:
            methods_with_forms.append({
                "method": method,
                "delete_form": RemoveSavedMethodForm(pk=method.id),
                "default_payment_form": SetDefaultPaymentForm(pk=method.id),
            })

        context["methods_with_forms"] = methods_with_forms
        return context


class DeleteMethodView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(PaymentMethods, pk=pk, user=request.user)
        address.delete()
        messages.success(request, "Payment method deleted successfully")
        return redirect("payment-methods")


class UpdateSavedMethodView(LoginRequiredMixin, CabinetContextMixin, UpdateView):
    model = PaymentMethods
    form_class = ChangeSavedMethod
    template_name = "payment_methods/method-update.html"
    success_url = reverse_lazy("payment-methods")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.helper.form_action = reverse("update-method", kwargs={"pk": self.object.pk})
        return form

    def get_queryset(self):
        return PaymentMethods.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Payment method updated successfully")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error.")
        return super().form_invalid(form)
