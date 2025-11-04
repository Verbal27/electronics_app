from django.urls import path
from src.website import views

urlpatterns = [
    path("", views.HomePageListView.as_view(), name="homepage"),
    path("product/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
    path(
        "category/<int:category_id>/",
        views.CategoryListView.as_view(),
        name="category_products",
    ),
    path(
        "subcategory/<int:subcategory_id>/",
        views.SubCategoryProductListView.as_view(),
        name="subcategory_products",
    ),
    path("cart/", views.CartListView.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"
    ),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
]
