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


class SavedAddressRadioSelect(forms.RadioSelect):
    template_name = "widgets/saved_addresses.html"


class ShippingRadioSelect(forms.RadioSelect):
    template_name = "widgets/shipping_radio.html"


class ShippingChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj


class OrderModelForm(ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    street = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Stefan cel Mare si Sfant 1"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Chisinau"}))
    state = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "CU"}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "2121"}))
    save_address = forms.BooleanField(required=False)
    phone = PhoneNumberField(region="MD", widget=forms.TextInput(attrs={"placeholder": "+373-00-000-000"}))
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
    payment_method = TypedChoiceField(widget=forms.RadioSelect,
                                      choices=[("1", "Cash"), ("2", "Debit Card"), ("3", "Credit Card")], initial="1")
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
        choices=[(y, str(y)) for y in range(current, current + 15)], coerce=int, required=False
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
            self.fields["saved_addresses"].choices = [
                (addr.id, f"{addr.street}, {addr.city}, {addr.state}, {addr.zipcode}")
                for addr in addresses
            ]
            self.fields["saved_addresses"].required = False
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
                        HTML("<div class='fw-bold fs-3'>Shipping Information</div>"),
                        css_class="d-flex align-items-baseline mb-4 gap-2",
                    ),
                ),
                Field("saved_addresses", css_class=""),
                Row(
                    Column(
                        Field("first_name", css_class="bg-input"),
                        css_class="form-group col-md-6 mb-0",
                    ),
                    Column(
                        Field("last_name", css_class="bg-input"),
                        css_class="form-group col-md-6 mb-0",
                    ),
                    Field("email", css_class="bg-input"),
                    Field("phone", css_class="phone bg-input"),
                    Field("street", css_class="bg-input"),
                    Div(
                        Field("city", css_class="bg-input d-inline-flex"),
                        Field("state", css_class="bg-input d-inline-flex"),
                        Field("zipcode", css_class="bg-input d-inline-flex"),
                        css_class="d-flex gap-2 w-100",
                    ),
                    "save_address",
                ),
                css_class="border border-1 rounded-4 bg-white p-4 mb-4",
            ),
            Div(
                Row(
                    Div(
                        Div(
                            HTML(
                                "<i class='fa-solid fa-box-open fs-4 text-light-blue'></i>"
                            ),
                            css_class="bg-light-blue p-2 border rounded-3",
                        ),
                        HTML("<div class='fw-bold fs-3'>Shipping Method</div>"),
                        css_class="d-flex align-items-baseline mb-4 gap-2",
                    ),
                ),
                HTML("{{ form.shipping }}"),
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
                        HTML("<div class='fw-bold fs-3'>Payment Information</div>"),
                        css_class="d-flex align-items-baseline mb-4 gap-2",
                    ),
                ),
                Field("payment_method", css_class="method-radio fw-medium"),
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
                    css_class="card-details",
                ),
                css_class="border border-1 rounded-4 bg-white p-4 my-4",
            ),
        )

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.user:
            order.user = self.user

        if commit:
            shipping = self.cleaned_data["shipping"]
            tax_rate = Decimal("0.08")
            tax = (Decimal(self.total) + shipping.price) * tax_rate
            total_amount = Decimal(self.total) + shipping.price + tax

            payment = Payment.objects.create(
                payment_method=self.cleaned_data["payment_method"],
                amount=total_amount,
                status="1",
            )

            if self.cleaned_data["save_address"]:
                SavedAddress.objects.update_or_create(
                    user=self.user,
                    first_name=self.cleaned_data["first_name"],
                    last_name=self.cleaned_data["last_name"],
                    email=self.cleaned_data["email"],
                    street=self.cleaned_data["street"],
                    city=self.cleaned_data["city"],
                    state=self.cleaned_data["state"],
                    zipcode=self.cleaned_data["zipcode"],
                    phone=self.cleaned_data["phone"],
                )

            order.payment = payment
            order.status = OrderStatus.PENDING
            order.shipping = shipping.code
            order.save()

            for item in self.cart_items:
                OrderItem.objects.create(
                    order_id=order.id,
                    product_id=int(item["id"]),
                    product_name=item["name"],
                    quantity=item["quantity"],
                    price=item["price"],
                )

        return order
