from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from ..core.models import ShippingOption, Product, ProductImage
from ..core.models.product import Specification


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
