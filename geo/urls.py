from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import register, calculate, get_user_slots, \
    get_user_poi, get_user_segment, get_user_cities

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', register),
    path('api/calculate/', calculate),
    path('api/user-city/', get_user_cities),
    path('api/user-slot/', get_user_slots),
    path('api/user-poi/', get_user_poi),
    path('api/user-segment/', get_user_segment)
]
