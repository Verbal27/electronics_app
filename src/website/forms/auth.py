from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from src.users.models import CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput,max_length=100,required=True)
    last_name = forms.CharField(widget=forms.TextInput,max_length=100,required=True)
    email = forms.EmailField(widget=forms.EmailInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
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


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
