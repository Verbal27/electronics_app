from .auth import RegisterView, UserLoginView, UserLogoutView
from .orders import OrderListView, AllOrderListView
from .account_info import AccountInfoView
from .addresses import AddressListView

__all__ = ["RegisterView", "UserLoginView", "UserLogoutView", "OrderListView", "AccountInfoView", "AddressListView",
           "AllOrderListView"]
