from django.urls import include, path

from src.users.views import RegisterView, UserLoginView, LogoutView
from src.website import views

urlpatterns = [
    path("", views.HomePageListView.as_view(), name="homepage"),
    path("products/", views.ProductsListView.as_view(), name="products"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("cabinet/", views.CabinetTemplateView.as_view(), name="cabinet"),
    path("search/", views.SearchListView.as_view(), name="search"),
    path("<int:pk>/", include([
        path("product/", views.ProductDetailView.as_view(), name="product_detail"),
        path("category/", views.CategoryListView.as_view(), name="category_products", ),
        path("subcategory/", views.SubCategoryProductListView.as_view(), name="subcategory_products", ),
    ])),
    path("cart/", include([
        path("", views.CartListView.as_view(), name="cart"),
        path("clear/", views.CartDropView.as_view(), name="clear_cart"),
        path("<int:product_id>/", include([
            path("add/", views.CartAddView.as_view(), name="add_to_cart", ),
            path("remove/", views.CartRemoveItemView.as_view(), name="remove_from_cart", ),
            path("update/", views.CartUpdateQuantityView.as_view(), name="update_cart", ),
        ]), ),
    ])),
    path("checkout/", include([
        path("", views.CheckoutCreateView.as_view(), name="checkout"),
    ]), )
]
