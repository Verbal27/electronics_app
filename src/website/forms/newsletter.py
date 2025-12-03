from crispy_forms.layout import Layout, Submit
from crispy_forms.helper import FormHelper
from django import forms

from src.core.components.website.inputs import Component, SimpleInput


class NewsletterForm(forms.Form):
    email = forms.EmailField(required=True, label="", widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "subscribe"
        self.helper.form_class = "newsletter-form d-inline-flex justify-content-center gap-2"
        self.helper.layout = Layout(
                Component(
                    component=SimpleInput(
                        name="email",
                        placeholder="Enter your email",
                        css_classes="newsletter-input",
                        input_type="text",
                    ),
                    field_name="email",
                ),
                Submit("subscribe", "Subscribe", css_class="btn btn-primary")
        )
