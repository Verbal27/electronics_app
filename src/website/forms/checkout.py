from datetime import date
from decimal import Decimal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Field, Div, HTML
from django import forms
from django.forms import ModelForm, TypedChoiceField
from phonenumber_field.formfields import PhoneNumberField

from src.core.constants import OrderStatus
from src.core.models import Order, Payment, OrderItem, ShippingOption
from src.core.models.order import SavedAddress


class PaymentMethodChoiceField(forms.RadioSelect):
    template_name = "widgets/payment_method_radio.html"


class AddressModeRadioSelect(forms.RadioSelect):
    template_name = "widgets/address_mode_radio.html"


class SavedAddressRadioSelect(forms.RadioSelect):
    template_name = "widgets/saved_addresses.html"


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
    address_mode = forms.ChoiceField(
        choices=[("saved", "Use a saved address"), ("new", "Enter a new address")],
        widget=AddressModeRadioSelect,
        required=True,
    )
    saved_addresses = forms.ChoiceField(
        widget=SavedAddressRadioSelect,
    )
    # noinspection PyTypeChecker
    shipping = ShippingChoiceField(
        queryset=ShippingOption.objects.filter(is_active=True),
        widget=ShippingRadioSelect,
        empty_label=None,
        initial=ShippingOption.objects.filter(is_active=True).first(),
    )
    payment_method = TypedChoiceField(
        widget=PaymentMethodChoiceField,
        choices=[("1", "Cash"), ("2", "Debit Card"), ("3", "Credit Card")],
        initial="1"
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
        if self.user:
            addresses = SavedAddress.objects.filter(user=self.user)
            if addresses.exists():
                self.fields["saved_addresses"].choices = [
                    (
                        addr.id,
                        f"{addr.first_name}"
                        f" {addr.last_name},"
                        f" {addr.phone},"
                        f" {addr.email},"
                        f" {addr.street},"
                        f" {addr.city},"
                        f" {addr.state},"
                        f" {addr.zipcode}",
                    )
                    for addr in addresses
                ]
                self.fields["saved_addresses"].required = False
                self.fields["address_mode"].initial = "saved"
            else:
                self.fields["address_mode"].initial = "new"
                self.fields.pop("saved_addresses")
        else:
            self.fields["address_mode"].initial = "new"
            self.fields.pop("saved_addresses")
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
                                "<i class='fa-solid fa-location-dot fs-4 text-light-blue'></i>"
                            ),
                            css_class="bg-light-blue p-2 border rounded-3",
                        ),
                        HTML("<div class='fw-medium fs-4'>Shipping Information</div>"),
                        css_class="d-flex align-items-baseline mb-4 gap-2",
                    ),
                ),
                Div(
                    HTML("{{form.address_mode}}"),
                    css_id="address_mode"
                ),
                Div(
                    Div(
                        HTML(
                            "{{form.saved_addresses}}"
                        ),
                        css_class="justify-content-center align-items-center flex-column"
                    ),
                    css_id="saved-address-block",
                    css_class="align-items-center gap-2",
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
                                "<i class='fa-solid fa-box-open fs-3 text-light-blue'></i>"
                            ),
                            css_class="bg-light-blue p-2 border rounded-3",
                        ),
                        HTML("<div class='fw-medium fs-4'>Shipping Method</div>"),
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
                                "<i class='fa-solid fa-credit-card fs-4 text-light-blue'></i>"
                            ),
                            css_class="bg-light-blue p-2 border rounded-3",
                        ),
                        HTML("<div class='fw-medium fs-4'>Payment Information</div>"),
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
                                """
                                <i class="fa-solid fa-lock text-muted"></i>
                                <div>Secure Payment</div>
                                """
                            ),
                            css_class="d-flex align-items-center fw-medium gap-2 align-items-baseline",
                        ),
                        Div(
                            HTML(
                                """
                                <div>Your payment information is encrypted and secure
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
        address_mode = cleaned_data.get("address_mode")
        saved_address = cleaned_data.get("saved_addresses")

        if address_mode == "saved":
            if not saved_address:
                self.add_error(
                    "saved_addresses",
                    "Please select a saved address or switch to entering a new address.",
                )
        else:
            required_fields = [
                "first_name",
                "last_name",
                "email",
                "street",
                "city",
                "state",
                "zipcode",
                "phone",
            ]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required.")

        payment_method = cleaned_data.get("payment_method")
        if payment_method in ("2", "3"):
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
            status="1",
        )

        mode = self.cleaned_data.get("address_mode")
        print(mode)
        print(self.cleaned_data)

        if mode == "saved" and self.cleaned_data.get("saved_addresses"):
            addr = SavedAddress.objects.get(
                id=self.cleaned_data["saved_addresses"],
                user=self.user,
            )
            order.first_name = addr.first_name
            order.last_name = addr.last_name
            order.email = addr.email
            order.street = addr.street
            order.city = addr.city
            order.state = addr.state
            order.zipcode = addr.zipcode
            order.phone = addr.phone

        else:
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
                    first_name=order.first_name,
                    last_name=order.last_name,
                    email=order.email,
                    street=order.street,
                    city=order.city,
                    state=order.state,
                    zipcode=order.zipcode,
                    phone=order.phone,
                )

        order.payment = payment
        order.status = OrderStatus.PENDING
        order.shipping = shipping.code
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
