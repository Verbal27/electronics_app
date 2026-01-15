from django.contrib.auth import authenticate, login
from django.db import transaction


class AuthServiceResult:
    def __init__(self, success, user=None, error=None):
        self.success = success
        self.user = user
        self.error = error

    @staticmethod
    def ok(user):
        return AuthServiceResult(True, user=user)

    @staticmethod
    def fail(error):
        return AuthServiceResult(False, error=error)


class AuthService:
    @transaction.atomic
    def register_user(self, request, form):
        if not form.is_valid():
            return AuthServiceResult.fail("invalid_form")

        user = form.save()
        password = form.cleaned_data.get("password1")

        authenticated = authenticate(request, username=user.username, password=password)
        if authenticated is None:
            return AuthServiceResult.fail("authentication_failed")

        login(request, authenticated)
        return AuthServiceResult.ok(authenticated)

    def login_user(self, request, form):
        if not form.is_valid():
            return AuthServiceResult.fail("invalid_form")

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return AuthServiceResult.fail("authentication_failed")

        login(request, user)
        return AuthServiceResult.ok(user)
