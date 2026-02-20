from django.urls import include, path
from src.users.views import (
    RegisterView,
    UserLoginView,
    UserLogoutView,
    OrderListView,
    AccountInfoView,
    AddressListView,
    AllOrderListView, ProfileImageUpdateView, OrderInfiniteScrollView, AllOrdersInfiniteScrollView, TwoFactorView,
    CustomPasswordChangeView, AdditionalDataView, ChangeSavedAddressView, DeleteAddressView
)
from src.website import views
from src.website.views.homepage import SubscribeView, SearchView

urlpatterns = [
    path("", views.HomePageListView.as_view(), name="homepage"),
    path("products/", views.ProductsListView.as_view(), name="products"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("cabinet/", include([
        path("orders/", include([
            path("", OrderListView.as_view(), name="orders"),
            path("all/", AllOrderListView.as_view(), name="all-orders"),
            path("infinite/", OrderInfiniteScrollView.as_view(), name="orders-infinite"),
            path("all-infinite/", AllOrdersInfiniteScrollView.as_view(), name="all-orders-infinite")
        ])),
        path("account-info/", include([
            path("", AccountInfoView.as_view(), name="account-info"),
            path("preferences-update/", AdditionalDataView.as_view(), name="preferences-update"),
            path("two-factor/", TwoFactorView.as_view(), name="two-factor"),
            path("password-change/", CustomPasswordChangeView.as_view(), name="password-change")
        ])),
        path("addresses/", include([
            path("", AddressListView.as_view(), name="addresses"),
            path("<int:pk>/update/", ChangeSavedAddressView.as_view(), name="address-update"),
            path("<int:pk>/delete/", DeleteAddressView.as_view(), name="delete-address")
        ])),
        # path("payment-methods/", include([
        #     path("",),
        # ])),
        path("update-image/", ProfileImageUpdateView.as_view(), name="update-image")
    ])),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("search/", SearchView.as_view(), name="search"),
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
            path("update-increase/", views.CartUpdateIncreaseQuantityView.as_view(), name="increase_quantity"),
            path("update-decrease/", views.CartUpdateDecreaseQuantityView.as_view(), name="decrease_quantity"),
        ]), ),
    ])),
    path("checkout/", include([
        path("", views.CheckoutCreateView.as_view(), name="checkout"),
        path("buynow/<int:pk>/", views.BuyNowView.as_view(), name="buy_now"),
        path("complete/<int:pk>/", views.CheckoutCompleteView.as_view(), name="complete"),
    ]), ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]
