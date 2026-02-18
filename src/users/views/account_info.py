from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.users.forms.account_info import UserDataForm


class AccountInfoView(LoginRequiredMixin, UpdateView):
    form_class = UserDataForm
    template_name = "account_info.html"
    success_url = reverse_lazy("account-info")

    def get_object(self):
        return self.request.user
