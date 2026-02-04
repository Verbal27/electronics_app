from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy

from src.core.components.website.icon import Icon
from src.core.components.website.iconbutton import IconButton
from src.users.models import CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Jane"}
        ),
        max_length=100,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Doe"}
        ),
        max_length=100,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "name@example.com"}
        ),
    )
    agreement = forms.BooleanField(required=True, label="I agree to the Terms of Service and Privacy Policy")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "register"
        self.fields["first_name"].label = ""
        self.fields["last_name"].label = ""
        self.fields["email"].label = ""
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].label = ""
        self.fields["password2"].help_text = "Minimum 8 characters with letters and numbers"
        self.fields["password1"].widget.attrs["placeholder"] = "*********"
        self.fields["password2"].widget.attrs["placeholder"] = "*********"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML(
                        """
                        <div class='fw-medium fs-6 mb-1 text-light-gray-dark'>
                            First Name
                        </div>
                        """
                    ),
                    Div(
                        HTML(
                            Icon(
                                icon_type=Icon.TYPES.USER,
                                css_classes="text-light-gray"
                            ),
                        ),
                        Field(
                            "first_name",
                            css_class="remove-outline border-0 bg-transparent",
                            wrapper_class="username-field-wrapper w-100",
                            show_errors=False,
                        ),
                        css_class="d-flex align-items-baseline border border-1 "
                                  "border-light-gray rounded-3 px-2 py-1 bg-light-grey-dark"
                    ),
                    css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    HTML(
                        """
                        <div class='fw-medium fs-6 mb-1 text-light-gray-dark'>
                            Last Name
                        </div>
                        """
                    ),
                    Div(
                        Field(
                            "last_name",
                            css_class="remove-outline border-0 bg-transparent",
                            wrapper_class="username-field-wrapper w-100"
                        ),
                        css_class="d-flex align-items-baseline border border-1 "
                                  "border-light-gray rounded-3 px-2 py-1 bg-light-grey-dark"
                    ),
                    css_class="form-group col-md-6 mb-0"
                ),
                css_class="mb-3"
            ),
            HTML(
                """
                <div class='fw-medium fs-6 mb-1 text-light-gray-dark'>
                    Email Address
                </div>
                """
            ),
            Div(
                HTML(
                    Icon(
                        icon_type=Icon.TYPES.ENVELOPE,
                        css_classes="text-light-gray"
                    ),
                ),
                Field(
                    "email",
                    css_class="remove-outline border-0 bg-transparent",
                    wrapper_class="username-field-wrapper w-100"
                ),
                css_class="d-flex align-items-baseline border border-1 "
                          "border-light-gray rounded-3 px-2 py-1 bg-light-grey-dark mb-3"
            ),
            HTML(
                """
                <div class="fw-semibold fs-6 mb-1 text-light-gray-dark">
                    Password
                </div>
                """
            ),
            Div(
                Field(
                    "password1",
                    css_class="password-field remove-outline border-0 bg-transparent",
                    wrapper_class="username-field-wrapper w-100 mt-3"
                ),
                HTML(
                    Icon(
                        icon_type=Icon.TYPES.EYE,
                        css_classes="text-light-gray show-hide-btn"
                    ),
                ),
                css_class="password-wrapper d-flex align-items-baseline border border-1 "
                          "border-light-gray rounded-3 px-2 py-1 bg-light-grey-dark mb-3"
            ),
            HTML(
                """
                <div class="fw-semibold fs-6 mb-1 text-light-gray-dark">
                    Repeat Password
                </div>
                """
            ),
            Field("password2", css_class="password-wrapper d-flex p-2 px-3 border-light-gray bg-light-grey-dark"),
            "agreement",
            Submit("submit", "Create Account", css_class="btn btn-primary btn-lg w-100"),
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
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "name@example.com"}),
        label="Email Address"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "**********"}),
        label="Password"
    )
    keep_signed = forms.BooleanField(required=False, label="Keep me signed in")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation w-100"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <div class='fw-medium fs-6 mb-1 text-light-gray-dark'>
                        Email Address
                    </div>
                    """
                ),
                Div(
                    HTML(
                        Icon(
                            icon_type=Icon.TYPES.ENVELOPE,
                            css_classes="text-light-gray"
                        ),
                    ),
                    Field(
                        "username",
                        css_class="remove-outline border-0 bg-transparent",
                        wrapper_class="username-field-wrapper w-100"
                    ),
                    css_class="d-flex align-items-baseline border border-1 "
                              "border-light-gray rounded-3 px-2 py-1 bg-light-grey-dark"
                ),
                Div(
                    HTML(
                        """
                        <div class='fw-medium fs-6 mb-1 mt-3 text-light-gray-dark'>
                            Password
                        </div>
                        """
                    ),
                    HTML(
                        """
                        <div class='fs-6 mb-1 mt-3'>
                            <a href="" class="text-decoration-none fw-semibold">Forgot?</a>
                        </div>
                        """
                    ),
                    css_class="d-flex justify-content-between w-100"
                ),
                Div(
                    Field(
                        "password",
                        css_class="password-field remove-outline border-0 bg-transparent",
                        wrapper_class="username-field-wrapper w-100 mt-3"
                    ),
                    HTML(
                        Icon(
                            icon_type=Icon.TYPES.EYE,
                            css_classes="text-light-gray show-hide-btn"
                        ),
                    ),
                    css_class="password-wrapper d-flex align-items-baseline border border-1 "
                              "border-light-gray rounded-3 px-2 py-1 bg-light-grey-dark"
                ),
                Field("keep_signed", wrapper_class="mt-3 text-light-gray-dark fw-semibold",
                      css_class=""),
                Submit(
                    "login",
                    "Sign In",
                    css_class="btn btn-primary rounded-3 w-100"
                ),
                css_class="d-flex flex-column"
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        if username and not CustomUser.objects.filter(email=username).exists():
            raise forms.ValidationError("User with that email does not exist.")

        return cleaned_data


class GoogleLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GoogleLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "google-login"
        self.helper.form_action = reverse_lazy("homepage")
        self.helper.layout = Layout(
            HTML(
                IconButton(
                    name="Google",
                    label="Google",
                    icon=Icon(Icon.TYPES.GOOGLE),
                    css_classes="d-flex flex-row-reverse align-items-baseline border border-1"
                                " rounded-3 border-light-grey bg-white px-5 py-2 gap-2 w-100 justify-content-center",
                    icon_css_classes=""
                )
            )
        )


class GitHubLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GitHubLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "github-login"
        self.helper.form_action = reverse_lazy("homepage")
        self.helper.layout = Layout(
            HTML(
                IconButton(
                    name="GitHub",
                    label="Gihub",
                    icon=Icon(Icon.TYPES.GITHUB),
                    css_classes="d-flex flex-row-reverse align-items-baseline border border-1"
                                " rounded-3 border-light-grey bg-white px-5 py-2 gap-2 w-100 justify-content-center",
                    icon_css_classes=""
                )
            )
        )


class UserLogoutForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLogoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse_lazy("logout")
        self.helper.layout = Layout(
            Submit("logout", "Logout", css_class="dropdown-item"),
        )
