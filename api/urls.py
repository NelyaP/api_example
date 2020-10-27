from django.urls import include, path
from rest_framework import routers
from .views import AccountView, OrderView, GroupView, PermissionView, \
    OrderDetailedView, OrderTypeView, OrderStatusView, AgeView, GenderView, \
    IncomeView, CityView, AccountFilterView, OrderItemView, \
    CityUserView, OrderTypeUserView


router = routers.DefaultRouter()

router.register(r'user', AccountView)
router.register(r'group', GroupView)
router.register(r'permission', PermissionView)
router.register(r'age', AgeView)
router.register(r'gender', GenderView)
router.register(r'income', IncomeView)
router.register(r'order', OrderView)
router.register(r'order-detail', OrderDetailedView)
router.register(r'order-type', OrderTypeView)
router.register(r'order-status', OrderStatusView)
router.register(r'city', CityView)
router.register(r'filter', AccountFilterView)
router.register(r'item', OrderItemView)
# user views #
router.register(r'user-city', CityUserView)
router.register(r'user-order-type', OrderTypeUserView)

urlpatterns = [
    path('', include(router.urls)),
]