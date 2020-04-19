from django.urls import include, path
from rest_framework import routers
from .views import AccountView, OrderView, GroupView, PermissionView, \
    OrderDetailedView, OrderTypeView, OrderStatusView

router = routers.DefaultRouter()

router.register(r'users', AccountView)
router.register(r'groups', GroupView)
router.register(r'permissions', PermissionView)
router.register(r'orders', OrderView)

router_ord = routers.DefaultRouter()
router_ord.register(r'details', OrderDetailedView)
router_ord.register(r'types', OrderDetailedView)
router_ord.register(r'statuses', OrderDetailedView)


urlpatterns = [
    path('', include(router.urls)),
    path('orders', include(router_ord.urls)),
]