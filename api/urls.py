from django.urls import include, path
from rest_framework import routers
from .views import AccountView, OrderView, GroupView, PermissionView, \
    OrderDetailedView

router = routers.DefaultRouter()

router.register(r'users', AccountView)
router.register(r'groups', GroupView)
router.register(r'permissions', PermissionView)
router.register(r'orders', OrderView)
router.register(r'ordersd', OrderDetailedView)

urlpatterns = [
    path('', include(router.urls)),
]