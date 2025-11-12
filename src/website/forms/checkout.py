from django import forms
from datetime import date
from django.forms import ModelForm, TypedChoiceField

from src.core.constants import OrderStatus
from src.core.models import Order, Payment, OrderItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class OrderModelForm(ModelForm):
    payment_method = TypedChoiceField(widget=forms.RadioSelect, choices=[("","Cash"),("","Debit Card"),("","Credit Card")])
    name_on_card = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    card_no = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
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
        exclude = ('payment',)

    def __init__(self, *args, cart_items=None, **kwargs):
            self.cart_items = cart_items
            super().__init__(*args, **kwargs)

            self.helper = FormHelper()
            self.helper.form_method = "POST"
            self.helper.form_class = "needs-validation"
            self.helper.attrs = {"novalidate":""}

            self.helper.layout = Layout(
                Submit('submit','Checkout', css_class='btn btn-primary btn-lg'),
            )

    def save(self, commit=True):
            order = super().save(commit=False)

            if commit:
                order.save()

                total = order.get_total()
                payment = Payment.objects.create(
                    method=self.payment_method,
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