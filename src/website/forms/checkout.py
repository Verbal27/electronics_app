from django import forms
from datetime import date
from django.forms import ModelForm, TypedChoiceField
from phonenumber_field.formfields import PhoneNumberField
from src.core.constants import OrderStatus
from src.core.models import Order, Payment, OrderItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Row, Column


class OrderModelForm(ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    address = forms.CharField()
    phone = PhoneNumberField(region="MD")
    payment_method = TypedChoiceField(widget=forms.RadioSelect, choices=[("cash","Cash"),("debit","Debit Card"),("credit","Credit Card")])
    name_on_card = forms.CharField(
        widget=forms.TextInput(),
    )
    card_no = forms.CharField(max_length=16, widget=forms.TextInput())
    expiration_date = forms.TypedChoiceField(
    choices=[(i, f"{i:02}") for i in range(1, 13)],
    coerce=int
    )
    current = date.today().year
    expiration_year = TypedChoiceField(
        choices=[(y, str(y)) for y in range(current, current + 15)], coerce=int
    )


    class Meta:
        model = Order
        exclude = ('payment','status','user')

    def __init__(self, *args, cart_items=None, **kwargs):
            self.cart_items = cart_items
            self.user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = "post"
            self.helper.form_class = "needs-validation"
            self.helper.attrs = {"novalidate":""}
            self.helper.layout = Layout(
                Fieldset(
                    "Personal Information",
                    Row(Column("first_name", default=self.user.first_name), Column("last_name",default=self.user.last_name)),
                    "email",
                    "address",
                    "phone",
                ),
                Fieldset(
                    "Payment Information",
                    "payment_method",
                    Row(Column("name_on_card"), Column("card_no")),
                    Row(Column("expiration_date"), Column("expiration_year")),
                ),
                Submit("submit", "Checkout", css_class="btn btn-primary btn-lg"),
            )

    def save(self, commit=True):
            order = super().save(commit=False)
            if self.user:
                order.user = self.user
            if commit:
                order.save()
                total = order.get_total()
                payment = Payment.objects.create(

                    method=self.cleaned_data['payment_method'],
                    amount=total,
                    status='pending'
                )
                order.payment = payment
                order.status = OrderStatus.PENDING
                order.save()

                for item in self.cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product_name,
                        quantity=item.quantity,
                        price=item.price,
                    )

            return order