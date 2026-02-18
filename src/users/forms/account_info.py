from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field
from src.users.models import CustomUser


class UserDataForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information",
                Div(
                    Field("first_name", css_class="bg-light-grey", wrapper_class="col"),
                    Field("last_name", css_class="bg-light-grey", wrapper_class="col"),
                    css_class="d-flex flex-wrap gap-2"
                ),
                Div(
                    Field("email", css_class="bg-light-grey", wrapper_class="col"),
                    Field("phone", css_class="bg-light-grey", wrapper_class="col"),
                    css_class="d-flex flex-wrap gap-2"
                )
            ),
            Submit("save", "Save changes", css_class="btn btn-add-to-cart")
        )
