from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, HTML
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from src.core.components.website import Icon
from src.core.components.website.iconbutton import IconButton
from src.core.components.website.span import Span
from src.users.models import CustomUser


class UserDataForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML(
                Span(
                    content="Personal Information",
                    css_classes="fs-6 fw-semibold"
                )
            ),
            Div(
                Field("first_name", css_class="bg-light-grey", wrapper_class="col fs-7 fw-medium"),
                Field("last_name", css_class="bg-light-grey", wrapper_class="col fs-7 fw-medium"),
                css_class="d-flex gap-2 mt-3 media-flex-col"
            ),
            Div(
                Field("email", css_class="bg-light-grey", wrapper_class="col fs-7 fw-medium"),
                Field("phone", css_class="bg-light-grey", wrapper_class="col fs-7 fw-medium"),
                css_class="d-flex gap-2 media-flex-col"
            ),
            Submit("save", "Save changes", css_class="btn btn-add-to-cart mt-2 fs-7")
        )


class AdditionalDataForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["order_updates", "promo_emails", "product_recommendations"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order_updates"].label = ""
        self.fields["promo_emails"].label = ""
        self.fields["product_recommendations"].label = ""
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "additional-form"
        self.helper.attrs = {
            "data-url": reverse("preferences-update")
        }
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        Span(
                            content="Order Updates",
                            css_classes="fs-6 fw-medium"
                        )
                    ),
                    HTML(
                        Span(
                            content="Receive emails about your order status",
                            css_classes="fs-8 text-muted fw-medium"
                        )
                    ),
                    css_class="d-flex flex-column"
                ),
                Field(
                    "order_updates",
                    css_class="form-check-input custom-tumbler",
                    wrapper_class="form-check form-switch",
                    id="order-update"
                ),
                css_class="d-flex justify-content-between mb-2"
            ),
            Div(
                Div(
                    HTML(
                        Span(
                            content="Promotional Emails",
                            css_classes="fs-6 fw-medium"
                        )
                    ),
                    HTML(
                        Span(
                            content="Get notified about deals and offers",
                            css_classes="fs-8 text-muted fw-medium"
                        )
                    ),
                    css_class="d-flex flex-column"
                ),
                Field(
                    "promo_emails",
                    css_class="form-check-input custom-tumbler",
                    wrapper_class="form-check form-switch"
                ),
                css_class="d-flex justify-content-between mb-2"
            ),
            Div(
                Div(
                    HTML(
                        Span(
                            content="Product Recommendations",
                            css_classes="fs-6 fw-medium"
                        )
                    ),
                    HTML(
                        Span(
                            content="Personalized product suggestions",
                            css_classes="fs-8 text-muted fw-medium"
                        )
                    ),
                    css_class="d-flex flex-column"
                ),
                Field(
                    "product_recommendations",
                    css_class="form-check-input custom-tumbler",
                    wrapper_class="form-check form-switch"
                ),
                css_class="d-flex justify-content-between mb-2"
            ),
        )


class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "old_password",
            "new_password1",
            "new_password2",
            Submit("submit", "Change Password",
                   css_class="btn btn-secondary text-dark bg-white border-1 border-light-grey fs-7")
        )

    def save(self, commit=True):
        user = super().save(commit=commit)

        user.last_password_change = timezone.now()

        if commit:
            user.save(update_fields=["last_password_change"])

        return user


class TwoFactorForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['two_factor_auth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('two-factor')
        self.helper.layout = Layout(
            Submit(
                "two_factor_toggle",
                "Disable" if self.instance.two_factor_auth else "Enable",
                css_class="btn btn-secondary text-dark bg-white border-1 border-light-grey fs-7"
            )
        )


class ProfileImageChange(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["profile_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_image"].widget.attrs.update({
            "class": "d-none",
            "id": "profileImageInput",
        })
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse_lazy("update-image")
        self.helper.form_class = "align-self-end"
        self.fields["profile_image"].label = ""
        self.helper.layout = Layout(
            Field("profile_image", wrapper_class="d-none"),
            HTML(
                IconButton(
                    name="change-profile-image",
                    btn_type="button",
                    icon=Icon(Icon.TYPES.CAMERA, css_classes="profile-image-change-icon"),
                    css_classes="profile-image-change border-0 bg-blue rounded-circle text-white",
                )
            )
        )
