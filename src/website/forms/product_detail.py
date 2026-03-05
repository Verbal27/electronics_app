from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div, HTML
from django import forms
from django.urls import reverse

from src.core.components.website import Icon
from src.core.components.website.button import Button
from src.core.components.website.span import Span
from src.core.models.product import ProductReview


class CustomRatingStarsWidget(forms.Widget):
    template_name = "widgets/stars_rating.html"


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, widget=CustomRatingStarsWidget, required=True)
    text = forms.CharField(max_length=500, min_length=10)

    class Meta:
        model = ProductReview
        fields = ["title", "text", "rating"]

    def __init__(self, *args, user=None, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.product = product
        self.helper = FormHelper()
        self.helper.form_class = "review-form"
        self.fields["rating"].label = ""
        self.fields["title"].label = "Review Title"
        self.fields["text"].label = "Review Body"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("post_review", args=[product])
        self.helper.layout = Layout(
            Div(
                HTML(
                    Span(
                        content="Overall rating",
                        css_classes="fw-semibold"
                    )
                ),
                Field("rating", name="rating"),
                Field(
                    "title",
                    placeholder="Summarize your experience",
                    css_class="bg-light-grey p-2 fs-7",
                    wrapper_class="fw-semibold"
                ),
                Field(
                    "text",
                    placeholder="What did you like or dislike? How was the performance?",
                    css_class="bg-light-grey pb-4 fs-7",
                    wrapper_class="fw-semibold"
                ),
                Div(
                    HTML(
                        Icon(
                            icon_type=Icon.TYPES.PLUS,
                            css_classes="text-first"
                        ),
                    ),
                    HTML(
                        Span(
                            content="Your review will be posted publicly after verification.",
                            css_classes="text-muted fs-8"
                        ),
                    ),
                    css_class="d-flex bg-lighter-blue align-items-baseline p-2 rounded-3 gap-2"
                ),
                css_class="p-4"
            ),
            Div(
                css_class="border-bottom w-100"
            ),
            Div(
                HTML(
                    Button(
                        label="Cancel",
                        style=Button.Styles.LIGHT,
                        id="cancel-btn",
                        css_class="border-light-gray text-dark fs-7",
                        **{
                            "data-bs-dismiss": 'modal',
                            "aria-label": "Close"
                        }
                    )
                ),
                Submit("submit_review", "Post Review", css_class="btn btn-primary px-4 fs-7"),
                css_class="d-flex justify-content-end p-3 gap-2"
            )
        )
