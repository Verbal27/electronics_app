from django.urls import include, path
from src.users.views import (
    RegisterView,
    UserLoginView,
    UserLogoutView,
    OrderListView,
    AccountInfoView,
    AddressListView,
    ProfileImageUpdateView, OrderInfiniteScrollView, TwoFactorView,
    CustomPasswordChangeView, AdditionalDataView, ChangeSavedAddressView, DeleteAddressView, PaymentListView,
    DeleteMethodView, OrderDetailView, AddPaymentView, SetDefaultCardView, UpdateSavedMethodView
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
            path("infinite-scroll/", OrderInfiniteScrollView.as_view(), name="orders-infinite"),
            path("<int:pk>/detail/", OrderDetailView.as_view(), name="order-detail"),
        ])),

        path("account/", include([
            path("", AccountInfoView.as_view(), name="account-info"),
            path("preferences/", AdditionalDataView.as_view(), name="preferences-update"),
            path("two-factor/", TwoFactorView.as_view(), name="two-factor"),
            path("password/", CustomPasswordChangeView.as_view(), name="password-change")
        ])),

        path("addresses/", include([
            path("", AddressListView.as_view(), name="addresses"),
            path("<int:pk>/", include([
                path("", ChangeSavedAddressView.as_view(), name="address-update"),
                path("delete/", DeleteAddressView.as_view(), name="delete-address")
            ]))
        ])),

        path("payment-methods/", include([
            path("", PaymentListView.as_view(), name="payment-methods"),
            path("add/", AddPaymentView.as_view(), name="add-payment-method"),
            path("<int:pk>/", include([
                path("", UpdateSavedMethodView.as_view(), name="update-method"),
                path("delete/", DeleteMethodView.as_view(), name="delete-method"),
                path("set-default/", SetDefaultCardView.as_view(), name="make-default")
            ]))
        ])),

        path("ajax/", include([
            path("profile/image/", ProfileImageUpdateView.as_view(), name="update-image")
        ]))
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
