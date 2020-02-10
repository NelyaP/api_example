from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orders', views.OrderView)

urlpatterns = [
    path('', include(router.urls))
]