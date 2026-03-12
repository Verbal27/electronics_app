from django import forms
from django.utils import timezone
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from ..core.constants.review import ProductReviewStatus
from ..core.models import ShippingOption, Product, ProductImage
from ..core.models.product import Specification, ProductReview


@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "delivery_time", "is_active")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 3


class ProductAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="product_description",
            ),
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageInline, SpecificationInline]
    list_display = ("name", "brand", "subcategory", "price", "quantity")
    list_filter = ("subcategory", "brand")
    search_fields = ("name", "brand")


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "rating",
        "moderation_status",
        "created_at",
        "moderated_by",
    )

    list_filter = (
        "moderation_status",
        "rating",
        "created_at",
    )

    list_select_related = ("product", "user")

    search_fields = (
        "product__name",
        "user__email",
        "title",
        "text",
    )

    readonly_fields = (
        "created_at",
        "moderated_at",
        "moderated_by",
    )

    actions = [
        "approve_reviews",
        "reject_reviews",
    ]

    def approve_reviews(self, request, queryset):
        queryset.update(
            moderation_status=ProductReviewStatus.APPROVED,
            moderated_at=timezone.now(),
            moderated_by=request.user,
        )

    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        queryset.update(
            moderation_status=ProductReviewStatus.REJECTED,
            moderated_at=timezone.now(),
            moderated_by=request.user,
        )

    reject_reviews.short_description = "Reject selected reviews"
