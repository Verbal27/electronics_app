from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from src.website.forms import RegisterForm, UserLoginForm, UserLogoutForm


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        self.object = form.save()
        user = self.object
        password = form.cleaned_data.get("password1")
        auth_user = authenticate(self.request, username=user.username, password=password)
        if auth_user is not None:
            login(self.request, auth_user)
            messages.success(self.request, "User created successfully")
        else:
            messages.error(self.request, "Authentication Failed")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "There was an error.")
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


    def get_success_url(self):
        return reverse_lazy("homepage")

    def post(self, request, *args, **kwargs):
        if "register" in request.POST:
            return redirect("register")
        return super().post(request, *args, **kwargs)


class UserLogoutView(LoginRequiredMixin,LogoutView):
    next_page = reverse_lazy("homepage")
    form_class = UserLogoutForm