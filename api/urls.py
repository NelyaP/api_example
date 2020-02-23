from django.urls import include, path
from rest_framework import routers
from .views import UserView, ReportView, OrderView, GroupView, PermissionView

router = routers.DefaultRouter()

router.register(r'users', UserView)
router.register(r'groups', GroupView)
router.register(r'permissions', PermissionView)
router.register(r'reports', ReportView)
router.register(r'orders', OrderView)

urlpatterns = [
    path('', include(router.urls)),
]