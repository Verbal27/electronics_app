from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, HTML
from django import forms
from django.urls import reverse


class AddToCartForm(forms.Form):
    def __init__(self, *args, product_id=None, **kwargs):
        super(AddToCartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("add_to_cart", args=[product_id])
        self.helper.layout = Layout(
            Submit("add_to_cart", "Add To Cart", css_class="btn btn-primary btn-add-to-cart"),
        )


class AddToCartDetailForm(forms.Form):
    quantity = forms.ChoiceField(initial=1, choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])

    def __init__(self, *args, product_id=None, **kwargs):
        super(AddToCartDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("add_to_cart", args=[product_id])
        self.helper.layout = Layout(
            Div(
                Div(
                    Field("quantity"),
                    css_class="d-flex d-flex-center align-items-center"
                ),
                css_class="mb-4"
            ),
            Submit("add_to_cart", "Add To Cart", css_class="btn btn-primary btn-add-to-cart"),
        )


class RemoveFromCartForm(forms.Form):
    def __init__(self, *args, product_id=None, **kwargs):
        super(RemoveFromCartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("remove_from_cart", args=[product_id])
        self.helper.layout = Layout(
            HTML("""
                <button type="submit" class="btn custom-delete-btn text-danger">
                    <i class='fa fa-trash'></i>
                </button>
            """)
        )


class UpdateCart(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=False)

    def __init__(self, *args, product_id=None, quantity=None, **kwargs):
        self.product_id = product_id
        initial = kwargs.pop('initial', {})
        if quantity is not None:
            initial['quantity'] = quantity
        kwargs['initial'] = initial

        super(UpdateCart, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("update_cart", args=[self.product_id])
        self.helper.layout = Layout(
            "quantity",
            Submit("update_cart", "Update", css_class="btn btn-primary btn-update-cart"),
        )


class DropCart(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DropCart, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "clear_cart"
        self.helper.layout = Layout(
            Submit("clear_cart", "Clear", css_class="btn btn-warning btn-block btn-lg"),
        )


class CheckoutForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_action = reverse("checkout")
        self.helper.layout = Layout(
            Submit("checkout", "Checkout", css_class="btn btn-warning btn-block btn-lg"),
        )
