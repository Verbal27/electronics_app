from django.urls import include, path
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
    path(
        "cart/",
        include(
            [
                path("", views.CartListView.as_view(), name="cart"),
                path(
                    "add/<int:product_id>/",
                    views.CartAddView.as_view(),
                    name="add_to_cart",
                ),
                path(
                    "remove/<int:product_id>/",
                    views.CartRemoveItemView.as_view(),
                    name="remove_from_cart",
                ),
                path(
                    "update/<int:product_id>/",
                    views.CartUpdateQuantityView.as_view(),
                    name="update_cart",
                ),
                path("clear/", views.CartDropView.as_view(), name="clear_cart"),
            ]
        ),
    ),
]
