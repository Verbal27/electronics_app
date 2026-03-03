from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.urls import reverse

from src.core.models.product import ProductReview


class CustomRatingField(forms.NumberInput):
    template_name = ""


class ReviewForm(forms.ModelForm):
    text = forms.CharField(max_length=500)
    rating = forms.CharField(widget=CustomRatingField)

    class Meta:
        model = ProductReview
        fields = ["title", "text", "rating"]

    def __init__(self, *args, user=None, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.product = product
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("post_review", args=[product])
        self.helper.layout = Layout(
            "rating",
            "title",
            "text",
            Submit("submit_review", "Submit", css_class="btn btn-secondary bg-dark text-white")
        )
