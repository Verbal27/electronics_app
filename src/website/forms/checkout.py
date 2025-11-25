from datetime import date
from decimal import Decimal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Row, Column, Field
from django import forms
from django.forms import ModelForm, TypedChoiceField
from phonenumber_field.formfields import PhoneNumberField

from src.core.constants import OrderStatus
from src.core.models import Order, Payment, OrderItem


class OrderModelForm(ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    address = forms.CharField()
    phone = PhoneNumberField(region="MD")
    payment_method = TypedChoiceField(widget=forms.RadioSelect,
                                      choices=[("1", "Cash"), ("2", "Debit Card"), ("3", "Credit Card")], initial="1")
    name_on_card = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )
    card_no = forms.CharField(max_length=16, widget=forms.TextInput(), required=False)
    expiration_date = forms.TypedChoiceField(
        choices=[(i, f"{i:02}") for i in range(1, 13)],
        coerce=int,
        required=False,
    )
    current = date.today().year
    expiration_year = TypedChoiceField(
        choices=[(y, str(y)) for y in range(current, current + 15)], coerce=int, required=False
    )

    class Meta:
        model = Order
        exclude = ('payment', 'status', 'user')

    def __init__(self, *args, cart_items=None, **kwargs):
        self.cart_items = kwargs.pop('cart_items', [])
        self.user = kwargs.pop('user', None)
        self.total = kwargs.pop('total', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = 'checkout'
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information",
                Row(
                    Column("first_name", css_class="form-group col-md-6 mb-0"),
                    Column("last_name", css_class="form-group col-md-6 mb-0"),
                ),
                "email",
                "address",
                Field("phone", css_class="phone"),
            ),
            Fieldset(
                "Payment Information",
                Field("payment_method", css_class="method-radio"),
                Fieldset(
                    "Card Details",
                    Row(
                        Column("name_on_card", css_class="form-group col-md-6 mb-0"),
                        Column("card_no", css_class="form-group col-md-6 mb-0"),
                    ),
                    Row(
                        Column("expiration_date", css_class="form-group col-md-6 mb-0"),
                        Column("expiration_year", css_class="form-group col-md-6 mb-0"),
                    ), css_class="card-details"),
            ),
            Submit("submit", "Checkout", css_class="btn btn-primary btn-lg"),
        )

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.user:
            order.user = self.user
        if commit:
            total = self.total
            payment = Payment.objects.create(
                payment_method=self.cleaned_data['payment_method'],
                amount=Decimal(total),
                status='1'
            )
            order.payment = payment
            order.status = OrderStatus.PENDING
            order.save()
            for item in self.cart_items:
                OrderItem.objects.create(
                    order_id=order.id,
                    product_id=int(item['pid']),
                    product_name=item['name'],
                    quantity=item['quantity'],
                    price=item['price'],
                )

        return order
