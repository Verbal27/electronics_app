from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms


class Search(forms.Form):

    def __init__(self, *args, **kwargs):
        super(Search, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.form_action = "search"
        self.helper.layout = Layout(
            Submit("search", "Search"),
        )
