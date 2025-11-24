from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Row, Column, Field, Div, HTML
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse

from src.users.models import CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput,max_length=100,required=True)
    last_name = forms.CharField(widget=forms.TextInput,max_length=100,required=True)
    email = forms.EmailField(widget=forms.EmailInput,required=True)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "register"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout(
            Fieldset(
                "Registration form",
                Row(
                    Column("first_name", css_class="form-group col-md-6 mb-0"),
                    Column("last_name", css_class="form-group col-md-6 mb-0"),
                ),
                "email",
                "password1",
                "password2"
            ),
            Submit("submit", "Register", css_class="btn btn-primary btn-lg"),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and first_name != first_name.capitalize():
            self.add_error("first_name", "First name must be capitalized.")

        if last_name and last_name != last_name.capitalize():
            self.add_error("last_name", "Last name must be capitalized.")

        return cleaned_data


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}

        self.helper.layout = Layout(
            HTML("<h3 class='mb-3'>Login form</h3>"),
            Div(Field("username"), css_class="form-group"),
            Div(Field("password", wrapper_class="pt-3"), css_class="form-group"),
            Div(
                Submit("login", "Login", css_class="btn btn-primary my-2 w-30 "),
            HTML("<p class='mb-3'>Not yet registered ?</p>"),
                Submit("register", "Register", css_class="btn btn-primary my-2 w-30"),
                css_class="form-group d-flex justify-content-between",)
        )


class UserLogoutForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLogoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("logout")
        self.helper.layout = Layout(
            Submit("logout", "Logout", css_class="dropdown-item"),
        )