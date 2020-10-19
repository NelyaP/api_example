from django.urls import include, path
from rest_framework import routers
from .views import AccountView, OrderView, GroupView, PermissionView, \
    OrderDetailedView, OrderTypeView, OrderStatusView, AgeView, GenderView, \
    IncomeView, CityView, AccountFilterView, SourcePropView, OrderItemView

router = routers.DefaultRouter()

router.register(r'users', AccountView)
router.register(r'groups', GroupView)
router.register(r'permissions', PermissionView)
router.register(r'age', AgeView)
router.register(r'gender', GenderView)
router.register(r'income', IncomeView)
router.register(r'orders', OrderView)
router.register(r'ordersdt', OrderDetailedView)
router.register(r'orderstp', OrderTypeView)
router.register(r'ordersst', OrderStatusView)
router.register(r'city', CityView)
router.register(r'filter', AccountFilterView)
router.register(r'item', OrderItemView)
router.register(r'source', SourcePropView)

urlpatterns = [
    path('', include(router.urls)),
]