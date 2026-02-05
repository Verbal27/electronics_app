from django import forms


class CustomPasswordWidget(forms.PasswordInput):
    template_name = 'widgets/custom_password.html'

    def __init__(self, icon=None, attrs=None):
        default_attrs = {
            "class": "form-control password-field bg-light-grey-dark",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
        self.icon = icon

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['icon'] = self.icon
        return context
