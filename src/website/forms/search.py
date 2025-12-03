from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django import forms

from src.core.components.website.inputs import SimpleInput


class Search(forms.Form):
    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(Search, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.form_action = "search"
        self.helper.form_class = "w-100 border-0 bg-transparent"
        self.helper.layout = Layout(
            HTML(
                SimpleInput(name="query", placeholder="Search products", css_classes="search-bar", input_type="text"),
            )
        )
