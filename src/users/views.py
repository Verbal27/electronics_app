from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from src.users.models import CustomUser
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
    success_url = reverse_lazy("homepage")



class CabinetTemplateView(TemplateView):
    template_name = "cabinet.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = CustomUser.objects.get(pk=user.pk)
        user_context = {
            "user": context,
        }
        return user_context

