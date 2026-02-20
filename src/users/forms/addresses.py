from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from django import forms
from django.urls import reverse

from src.core.components.website import Icon
from src.core.components.website.iconbutton import IconButton
from src.core.models.order import SavedAddress


class ChangeSavedAddress(forms.ModelForm):
    class Meta:
        model = SavedAddress
        fields = ["first_name", "last_name", "street", "city", "state", "zipcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "first_name",
            "last_name",
            "street",
            "city",
            "state",
            "zipcode",
            Submit("submit", "Save Changes", css_classes="btn btn-secondary bg-white")
        )


class RemoveSavedAddressForm(forms.Form):

    def __init__(self, pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("delete-address", args=[pk])
        self.helper.layout = Layout(
            HTML(
                IconButton(
                    name="delete address",
                    icon=Icon(Icon.TYPES.DELETE),
                    btn_type="submit",
                    css_classes="border-0 bg-transparent",
                    icon_css_classes=""
                )
            )
        )
