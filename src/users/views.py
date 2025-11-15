from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from src.core.models import Order
from src.website.forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data.get("password1")
        auth_user = authenticate(self.request, username=user.username, password=password)
        if user is not None:
            login(self.request, auth_user)
            messages.success(self.request, "User created successfully")
            return redirect(reverse_lazy("homepage"))
        else:
            messages.error(self.request, "Authentication Failed")
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error.")
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("homepage")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("homepage")



class CabinetTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cabinet.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user:
            orders = (
                Order.objects.filter(user=user)
                .select_related("payment")
                .prefetch_related("items")
            )
            context["orders"] = orders
            return context
        else:
            return redirect_to_login(self.login_url)


