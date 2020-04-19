from django.urls import include, path
from rest_framework import routers
from .views import AccountView, OrderView, GroupView, PermissionView, \
    OrderDetailedView, OrderTypeView, OrderStatusView

router = routers.DefaultRouter()

router.register(r'users', AccountView)
router.register(r'groups', GroupView)
router.register(r'permissions', PermissionView)
router.register(r'orders', OrderView)
router.register(r'orders/details', OrderDetailedView)
router.register(r'orders/types', OrderDetailedView)
router.register(r'orders/statuses', OrderDetailedView)

urlpatterns = [
    path('', include(router.urls)),
]