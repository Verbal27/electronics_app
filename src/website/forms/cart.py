from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Button
from django import forms
from django.urls import reverse

from src.core.components.website.icon import Icon
from src.core.components.website.iconbutton import IconButton
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

    def __init__(self, *args, product_id=None, product=None, current_qty=0, **kwargs):
        super().__init__(*args, **kwargs)

        max_qty = product.quantity if product else 9999

        self.fields["quantity"].widget = forms.NumberInput(
            attrs={
                "class": "col col-md-4 d-flex justify-content-center mx-md-2 "
                "border-0 bg-transparent text-dark fw-semibold text-center",
                "style": "pointer-events: none; display: inline-flex;",
                "min": "1",
                "id": f"quantity-{product_id}",
                "data-product-id": str(product_id),
                "data-max": str(max_qty),
                "data-in-cart": str(current_qty),
                "value": "1",
            }
        )

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("add_to_cart", args=[product_id])
        self.helper.attrs = {"id": "product-detail-form"}

        self.helper.layout = Layout(
            Div(
                Button(
                    "decrease_quantity",
                    "-",
                    css_class="btn bg-white border rounded-3 text-dark qty-decrease",
                    type="button"
                ),
                "quantity",
                Button(
                    "increase_quantity",
                    "+",
                    css_class="btn bg-white border rounded-3 text-dark qty-increase",
                    type="button"
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
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("remove_from_cart", args=[product_id])

        self.helper.layout = Layout(
            Div(
                IconButton(
                    name="remove_from_cart",
                    icon=Icon(Icon.TYPES.DELETE),
                    css_classes="btn btn-delete bg-transparent text-muted fw-normal text-center"
                ),
                css_class="d-flex align-items-center",
            )
        )


class UpdateCart(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=False)

    def __init__(self, *args, product_id=None, quantity=None, **kwargs):
        self.product_id = product_id
        initial = kwargs.pop('initial', {})
        if quantity is not None:
            initial['quantity'] = quantity
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

        self.fields["quantity"].widget = forms.NumberInput(
            attrs={
                "class": "qtty border-0 p-0",
                "style": "pointer-events: none;",
                "min": "1",
                "id": "quantity",
                "name": "quantity",
            }
        )
        self.fields["quantity"].label = ""
        self.fields["quantity"].widget.attrs.update(
            {
                "data-product-id": str(self.product_id),
            }
        )
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("update_cart", args=[self.product_id])
        self.helper.form_class = "qty-form"
        self.helper.attrs = {
            "data-update-url": reverse("update_cart", args=[self.product_id]),
        }
        self.helper.layout = Layout(
            Div(
                Button("decrease_quantity", "-", css_class="btn bg-white border rounded-3 text-dark qty-decrease"),
                "quantity",
                Button("increase_quantity", "+", css_class="btn bg-white border rounded-3 text-dark qty-increase"),
                css_class="d-flex align-items-center gap-2",
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
            IconButton(
                name="checkout",
                label="Proceed to checkout",
                icon=Icon(Icon.TYPES.CHECKOUT),
                icon_css_classes="text-white",
                css_classes="btn bg-dark border-0 text-white w-100 text-wrap my-2 p-2"
            ),
        )


class PromoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PromoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "add_promo"
        self.helper.form_class = "row align-items-center align-items-center gap-1 promo-form"
        self.helper.layout = Layout(
            Div(
                HTML(Icon(icon_type=Icon.TYPES.PROMO)),
                HTML(
                    SimpleInput(
                        name="promo",
                        placeholder="Enter code",
                        css_classes="col-12 col-md-8 input-group-sm form-control"
                                    " bg-transparent border-0 p-2 m-0 promo-in",
                        input_type="text",
                    ),
                ),
                css_class="col promo-input d-flex rounded-3 border-0"
                          " bg-body-secondary px-3 text-muted align-items-center"),
            Submit(
                "apply_promo",
                "Apply",
                css_class="col-12 col-md-4 btn btn-primary border-2 "
                          "border-light-subtle bg-white text-dark fw-semibold promo-submit"
            ),
        )
