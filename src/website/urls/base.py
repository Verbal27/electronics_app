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
]
