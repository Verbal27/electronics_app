from datetime import date
from decimal import Decimal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Field, Div, HTML
from django import forms
from django.forms import ModelForm, TypedChoiceField
from phonenumber_field.formfields import PhoneNumberField

from src.core.components.website.icon import Icon
from src.core.constants import OrderStatus, PaymentStatus
from src.core.models import Order, Payment, OrderItem, ShippingOption
from src.core.models.order import SavedAddress


class PaymentMethodChoiceField(forms.RadioSelect):
    template_name = "widgets/payment_method_radio.html"


class ShippingRadioSelect(forms.RadioSelect):
    template_name = "widgets/shipping_radio.html"


class ShippingChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj


class OrderModelForm(ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    street = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Stefan cel Mare si Sfant 1"}
        ),
        required=False
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Chisinau"}
        ),
        required=False
    )
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "CU"}
        ),
        required=False)
    zipcode = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "2121"}
        ),
        required=False
    )
    save_address = forms.BooleanField(required=False)
    phone = PhoneNumberField(
        region="MD",
        widget=forms.TextInput(
            attrs={"placeholder": "+373-00-000-000"}
        ),
        required=False
    )
    # noinspection PyTypeChecker
    shipping = ShippingChoiceField(
        queryset=ShippingOption.objects.filter(is_active=True),
        widget=ShippingRadioSelect,
        empty_label=None,
    )
    payment_method = TypedChoiceField(
        widget=PaymentMethodChoiceField,
        choices=[("1", "Cash"), ("2", "Debit/Credit Card")],
        initial="1",
        coerce=int
    )
    name_on_card = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(), required=False)
    expiration_date = forms.TypedChoiceField(
        choices=[(i, f"{i:02}") for i in range(1, 13)],
        coerce=int,
        required=False,
    )
    current = date.today().year
    expiration_year = TypedChoiceField(
        choices=[(y, str(y)) for y in range(current, current + 15)],
        coerce=int,
        required=False
    )
    cvv = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )

    class Meta:
        model = Order
        exclude = ('payment', 'status', 'user')

    def __init__(self, *args, **kwargs):
        self.cart_items = kwargs.pop('cart_items', [])
        self.user = kwargs.pop('user', None)
        self.total = kwargs.pop('total', None)
        self.grand_total = kwargs.pop('grand_total', None)
        self.tax = kwargs.pop('tax', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        active_shipping = ShippingOption.objects.filter(is_active=True).first()
        if active_shipping:
            self.fields["shipping"].initial = active_shipping
        self.fields["shipping"].label = ""
        self.fields["payment_method"].label = ""
        self.fields["save_address"].label = "Save this address for future use"
        self.fields["zipcode"].label = "Zip Code"
        self.fields["cvv"].label = "CVV"
        self.helper.form_method = "post"
        self.helper.form_action = 'checkout'
        self.helper.form_id = "checkout-form"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout(
            Div(
                Row(
                    Div(
                        Div(
                            HTML(
                                Icon(
                                    icon_type=Icon.TYPES.MAP_POINTER,
                                    css_classes="fs-4 text-light-blue"
                                ),
                            ),
                            css_class="bg-light-blue p-2 border rounded-3",
                        ),
                        Div(HTML("Shipping Information"), css_class="fw-medium fs-4"),
                        css_class="d-flex align-items-baseline mb-4 gap-2",
                    ),
                ),
                Div(
                    Row(
                        Column(Field("first_name", css_class="bg-input")),
                        Column(Field("last_name", css_class="bg-input")),
                        Field("email", css_class="bg-input"),
                        Field("phone", css_class="bg-input"),
                        Field("street", css_class="bg-input"),
                        Div(
                            Field("city", css_class="bg-input"),
                            Field("state", css_class="bg-input"),
                            Field("zipcode", css_class="bg-input"),
                            css_class="d-flex gap-2",
                        ),
                        "save_address",
                    ),
                    css_id="new-address-block",
                ),
                css_class="border border-1 rounded-4 bg-white p-4 mb-4",
            ),
            Div(
                Row(
                    Div(
                        Div(
                            HTML(
                                Icon(
                                    icon_type=Icon.TYPES.DELIVERY_MODE,
                                    css_classes="fs-3 text-light-blue"
                                ),
                            ),
                            css_class="bg-light-blue p-2 border rounded-3",
                        ),
                        Div(HTML("Shipping Method"), css_class="fw-medium fs-4"),
                        css_class="d-flex align-items-baseline mb-4 gap-2",
                    ),
                ),
                Div(
                    HTML(
                        "{{ form.shipping }}"
                    ),
                    css_id="shipping-form",
                ),
                css_class="border border-1 rounded-4 bg-white p-4 my-4",
            ),
            Div(
                Row(
                    Div(
                        Div(
                            HTML(
                                Icon(
                                    icon_type=Icon.TYPES.CARD,
                                    css_classes="fs-4 text-light-blue"
                                ),
                            ),
                            css_class="bg-light-blue p-2 border rounded-3",
                        ),
                        Div(HTML("Payment Information"), css_class="fw-medium fs-4"),
                        css_class="d-flex align-items-baseline mb-4 gap-2",
                    ),
                ),
                Div(HTML("{{form.payment_method}}"), css_id="method-radio"),
                Fieldset(
                    "Card Details",
                    Field(
                        "card_number", css_class="form-group bg-input mb-0 fw-medium"
                    ),
                    Row(
                        Column(
                            Field(
                                "expiration_date",
                                css_class="form-group mb-0 bg-input fw-medium",
                            )
                        ),
                        Column(
                            Field(
                                "expiration_year",
                                css_class="form-group mb-0 bg-input fw-medium",
                            )
                        ),
                        Column(
                            Field("cvv", css_class="form-group mb-0 bg-input fw-medium")
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
                css_class="border border-1 rounded-4 bg-white p-4 my-4",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        required_fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "street",
            "city",
            "state",
            "zipcode",
        ]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This field is required.")

        payment_method = cleaned_data.get("payment_method")
        if payment_method == 2:
            card_fields = [
                "card_number",
                "expiration_date",
                "expiration_year",
                "cvv",
                "name_on_card",
            ]
            for field in card_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required for card payments.")

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)

        if self.user:
            order.user = self.user

        if not commit:
            return order

        shipping = self.cleaned_data["shipping"]
        subtotal = Decimal(self.total or 0)
        tax_rate = Decimal("0.08")

        tax = (subtotal + shipping.price) * tax_rate
        total_amount = subtotal + shipping.price + tax

        payment = Payment.objects.create(
            payment_method=self.cleaned_data["payment_method"],
            amount=total_amount,
            status=PaymentStatus.PENDING,
        )

        order.first_name = self.cleaned_data["first_name"]
        order.last_name = self.cleaned_data["last_name"]
        order.email = self.cleaned_data["email"]
        order.street = self.cleaned_data["street"]
        order.city = self.cleaned_data["city"]
        order.state = self.cleaned_data["state"]
        order.zipcode = self.cleaned_data["zipcode"]
        order.phone = self.cleaned_data["phone"]

        if self.cleaned_data.get("save_address") and self.user:
            SavedAddress.objects.update_or_create(
                user=self.user,
                defaults={
                    "first_name": order.first_name,
                    "last_name": order.last_name,
                    "email": order.email,
                    "street": order.street,
                    "city": order.city,
                    "state": order.state,
                    "zipcode": order.zipcode,
                    "phone": order.phone,
                },
            )

        order.payment = payment
        order.status = OrderStatus.PENDING
        order.shipping = shipping
        order.save()

        for item in self.cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=int(item["id"]),
                product_name=item["name"],
                quantity=item["quantity"],
                price=item["price"],
            )

        return order
