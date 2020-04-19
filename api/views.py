from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import Group, Permission
from .models import Account, Order, \
    OrderType, OrderStatus
from django.contrib.auth.models import Group, Permission
from .serializers import AccountSerializer, OrderSerializer, \
    GroupSerializer, PermissionSerializer, OrderDetailedSerializer, \
        OrderTypeSerializer, OrderStatusSerializer

from utils.pwd_generators import generate_20char_pwd
from django.contrib.auth import get_user_model

class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class OrderTypeView(viewsets.ModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer

class OrderStatusView(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailedView(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderDetailedSerializer

class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermissionView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def register(request):
    data = request.data
    username = data["username"]
    phone = data["phone"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    company = data["company"]
    message = "Processing"
    User = get_user_model()
    password = generate_20char_pwd()
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password, phone=phone, first_name=first_name, last_name=last_name, email=email, company=company)
        # send email
        return Response(status=status.HTTP_201_CREATED)
    else:
        message = "user_exists"

    err = {
        "error": message
    }
    return Response(err, status=status.HTTP_400_BAD_REQUEST)