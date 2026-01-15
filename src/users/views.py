from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.website.forms import RegisterForm, UserLoginForm, UserLogoutForm
from src.website.services.auth import AuthService


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        service = AuthService()
        result = service.register_user(self.request, form)

        if result.success:
            messages.success(self.request, "User created successfully")
            return redirect(self.get_success_url())

        if result.error == "invalid_form":
            messages.error(self.request, "Invalid data.")
        elif result.error == "authentication_failed":
            messages.error(self.request, "Authentication error.")
        else:
            messages.error(self.request, "Unexpected error.")

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "There was an error.")
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        service = AuthService()
        result = service.login_user(self.request, form=form)

        if result.success:
            messages.success(self.request, "User logged in.")
            return redirect(self.get_success_url())

        if result.error == "invalid_form":
            messages.error(self.request, "Invalid data.")
            return redirect("login")

        if result.error == "authentication_failed":
            messages.error(self.request, "Invalid username or password.")
            return redirect("login")

        messages.error(self.request, "Unexpected login error.")
        return redirect("login")

    def get_success_url(self):
        return reverse_lazy("homepage")

    def post(self, request, *args, **kwargs):
        if "register" in request.POST:
            return redirect("register")
        return super().post(request, *args, **kwargs)


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("homepage")
    form_class = UserLogoutForm
