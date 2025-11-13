from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from src.website.forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "User created successfully")
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
        if user.is_authenticated:
            context.update({
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            })
            return context
        else:
            return redirect_to_login(self.login_url)


