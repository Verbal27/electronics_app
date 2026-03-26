from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from src.core.components.cabinet_context import CabinetContextMixin
from src.users.forms import (
    UserDataForm,
    ProfileImageChange,
    AdditionalDataForm,
    TwoFactorForm,
    ChangePasswordForm
)


class AccountInfoView(LoginRequiredMixin, CabinetContextMixin, UpdateView):
    form_class = UserDataForm
    template_name = "account_info.html"
    success_url = reverse_lazy("account-info")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_password_change = self.request.user.last_password_change \
            if self.request.user.last_password_change is not None \
            else self.request.user.date_joined
        print(last_password_change)

        context.update({
            "last_password_change": last_password_change,
            "additional_form": AdditionalDataForm(instance=self.request.user),
            "security_form": TwoFactorForm(instance=self.request.user),
        })

        return context


class ProfileImageUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        form = ProfileImageChange(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile image updated successfully")
        else:
            messages.error(request, "Error updating profile image")

        return redirect("account-info")


class AdditionalDataView(LoginRequiredMixin, View):

    ALLOWED_FIELDS = {
        "order_updates",
        "promo_emails",
        "product_recommendations"
    }

    def post(self, request):
        field = request.POST.get("field")
        value = request.POST.get("value")

        if field not in self.ALLOWED_FIELDS:
            return JsonResponse({"success": False}, status=400)

        user = request.user
        setattr(user, field, value == "true")
        user.save(update_fields=[field])

        return JsonResponse({"success": True})


class TwoFactorView(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        user.two_factor_auth = not user.two_factor_auth
        user.save()
        return redirect(reverse_lazy("account-info"))


class CustomPasswordChangeView(LoginRequiredMixin, CabinetContextMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = "password_change.html"
    success_url = reverse_lazy("account-info")
