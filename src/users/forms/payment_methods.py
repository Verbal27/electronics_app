import uuid
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Field, Column, Row, Fieldset
from django import forms
from django.forms import TypedChoiceField
from django.urls import reverse

from src.core.components.website import Icon
from src.core.components.website.iconbutton import IconButton
from src.core.constants.payment import CardTypes
from src.core.models.payment import PaymentMethods


class AddNewMethod(forms.ModelForm):
    card_number = forms.CharField(min_length=16)
    expire_month = forms.TypedChoiceField(
        choices=[(i, f"{i:02}") for i in range(1, 13)],
        coerce=int,
        required=False,
    )
    current = date.today().year
    expire_year = TypedChoiceField(
        choices=[(y, str(y)) for y in range(current, current + 15)],
        coerce=int,
        required=False
    )

    class Meta:
        model = PaymentMethods
        fields = ["name_on_card", "expire_month", "expire_year"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "add-payment-method"
        self.helper.layout = Layout(
            Fieldset(
                "Card Details",
                Field(
                    "card_number", css_class="form-group bg-input mb-0 fw-medium"
                ),
                Row(
                    Column(
                        Field(
                            "expire_month",
                            css_class="form-group mb-0 bg-input fw-medium",
                        )
                    ),
                    Column(
                        Field(
                            "expire_year",
                            css_class="form-group mb-0 bg-input fw-medium",
                        )
                    ),
                ),
                Field(
                    "name_on_card", css_class="form-group bg-input mb-0 fw-medium"
                ),
                Div(
                    Div(
                        HTML(
                            Icon(
                                icon_type=Icon.TYPES.SECURE,
                                css_classes="text-muted"
                            ),
                        ),
                        HTML("Secure Payment"),
                        css_class="d-flex align-items-center fw-medium gap-2 align-items-baseline",
                    ),
                    Div(
                        HTML(
                            """
                            Your payment information is encrypted and secure
                            """
                        ),
                        css_class="d-flex align-items-center fw-medium text-muted",
                    ),
                    css_class="d-flex border rounded-3 bg-light-grey border-0 flex-column p-4",
                ),
                css_class="card-details",
            ),
            Submit("submit", "Save Card", css_class="btn btn-secondary bg-white text-dark mt-3")
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        card_number = self.cleaned_data["card_number"]

        instance.user = self.user
        instance.token = "pm_" + uuid.uuid4().hex
        instance.last_4 = card_number[-4:]
        instance.card_type = self.detect_brand(card_number)
        instance.is_default = not PaymentMethods.objects.filter(user=self.user, is_default=True).exists()

        if commit:
            instance.save()

        return instance

    def detect_brand(self, number):
        if number.startswith("4"):
            return CardTypes.VISA
        elif number.startswith(("51", "52", "53", "54", "55")):
            return CardTypes.MASTERCARD
        elif number.startswith(("34", "37")):
            return CardTypes.AMEX
        return 0


class ChangeSavedMethod(forms.ModelForm):
    masked_last_4 = forms.CharField(
        label="Card number",
        required=False,
        disabled=True,
    )

    class Meta:
        model = PaymentMethods
        fields = ["name_on_card", "card_type", "expire_month", "expire_year", "is_default"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["is_default"].label = "Set as default"
        self.helper = FormHelper()
        if self.instance and self.instance.pk:
            self.initial["masked_last_4"] = f"**** **** **** {self.instance.last_4}"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Card Details",
                "name_on_card",
                "masked_last_4",
                "card_type",
                "expire_month",
                "expire_year",
                "is_default",
            ),
            Submit("submit", "Save Changes", css_classes="btn btn-secondary bg-white text-dark")
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.is_default:
            PaymentMethods.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(pk=instance.pk).update(is_default=False)

        else:
            if not PaymentMethods.objects.filter(user=self.user, is_default=True).exclude(pk=instance.pk).exists():
                instance.is_default = True

        if commit:
            instance.save()

        return instance


class RemoveSavedMethodForm(forms.Form):

    def __init__(self, pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("delete-method", args=[pk])
        self.helper.layout = Layout(
            HTML(
                IconButton(
                    name="delete method",
                    icon=Icon(Icon.TYPES.DELETE),
                    btn_type="submit",
                    css_classes="border-0 bg-transparent",
                    icon_css_classes=""
                )
            )
        )


class SetDefaultForm(forms.Form):

    def __init__(self, pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("make-default", args=[pk])
        self.helper.layout = Layout(
            Submit("submit", "Set as default", css_class="btn btn-secondary text-dark bg-white w-100 my-1 fs-7")
        )
