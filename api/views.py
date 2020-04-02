from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Order, \
    OrderType, OrderStatus

from django.contrib.auth.models import Group, Permission
from .serializers import UserSerializer, OrderSerializer, \
    GroupSerializer, PermissionSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermissionView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer