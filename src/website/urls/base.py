from django.urls import path
from src.website import views

urlpatterns = [
    path("", views.HomePageListView.as_view(), name="homepage"),
    path("product/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
]
