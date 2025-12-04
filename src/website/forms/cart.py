from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, HTML
from crispy_forms.templatetags.crispy_forms_field import css_class
from django import forms
from django.urls import reverse

from src.core.components.website.inputs import SimpleInput


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
    quantity = forms.IntegerField(min_value=1, required=False, initial=1)

    def __init__(self, *args, product_id=None, **kwargs):
        super(AddToCartDetailForm, self).__init__(*args, **kwargs)
        self.fields["quantity"].widget = forms.NumberInput(
            attrs={
                "class": "col col-md-4 d-flex justify-content-center mx-md-2 border-0 bg-transparent text-dark fw-semibold text-center",
                "style": "pointer-events: none;display: inline-flex;",
                "min": "1",
                "id": "quantity",
            }
        )
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("add_to_cart", args=[product_id])
        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <button type="button" class=" btn bg-white border rounded-3 text-dark mt-3 qty-decrease d-flex justify-content-center px-3">-</button>
                    """
                ),
                "quantity",
                HTML(
                    """
                    <button type="button" class=" btn bg-white border rounded-3 text-dark mt-3 qty-increase d-flex justify-content-center px-3">+</button>
                    """
                ),
                css_class="d-flex align-items-center gap-2",
            ),
            Submit(
                "add_to_cart",
                "Add To Cart",
                css_class="btn btn-primary btn-update-cart d-inline-block h-100",
            ),
        )


class RemoveFromCartForm(forms.Form):
    def __init__(self, *args, product_id=None, **kwargs):
        super(RemoveFromCartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("remove_from_cart", args=[product_id])
        self.helper.layout = Layout(
            HTML("""
                <button type="submit" class="btn custom-delete-btn text-muted">
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

        self.fields["quantity"].widget = forms.NumberInput(
            attrs={
                "class": "col col-md-4 d-flex justify-content-center mx-md-2 border-0 bg-transparent text-dark fw-semibold text-center",
                "style": "pointer-events: none;display: inline-flex;",
                "min": "1",
                "id": "quantity",
            }
        )
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("update_cart", args=[self.product_id])
        self.helper.form_class = "d-flex justify-content-around align-items-baseline gap-3"
        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <button type="button" class=" btn bg-white border rounded-3 text-dark mt-3 qty-decrease d-flex justify-content-center px-3">-</button>
                    """
                ),
                "quantity",
                HTML(
                    """
                    <button type="button" class=" btn bg-white border rounded-3 text-dark mt-3 qty-increase d-flex justify-content-center px-3">+</button>
                    """
                ),
                css_class="d-flex align-items-center gap-2",
            ),
            Submit(
                "update_cart", "Update", css_class="btn btn-primary btn-update-cart d-inline-block h-100"
            ),
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
            Submit("checkout", "Proceed to checkout", css_class="btn btn-primary border-1 border-light-subtle bg-dark text-white w-100 my-2"),
        )


class PromoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PromoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "add_promo"
        self.helper.layout = Layout(
            Div(
            HTML("<i class='d-flex fa-solid fa-tag align-items-center'></i>"),
                    HTML(
                    SimpleInput(
                        name="promo",
                        placeholder="Enter code",
                        css_classes="input-group-sm form-control bg-transparent border-0",
                        input_type="text",
                    ),
                ),
            css_class="col promo-input d-inline-flex rounded-3 border-0 bg-body-secondary"),
            Submit("apply_promo", "Apply" , css_class="col-md-4 btn btn-primary border-2 border-light-subtle bg-white text-dark fw-semibold"),
        )