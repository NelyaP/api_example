from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import Group, Permission
from .models import Account, Order, \
    OrderType, OrderStatus, Age, Gender, Income, City, AccountFilter
from django.contrib.auth.models import Group, Permission
from .serializers import AccountSerializer, OrderSerializer, \
    GroupSerializer, PermissionSerializer, OrderDetailedSerializer, \
        OrderTypeSerializer, OrderStatusSerializer, AgeSerializer, \
        GenderSerializer, IncomeSerializer, CitySerializer, AccountFilterSerializer

from utils.pwd_generators import generate_20char_pwd
from django.contrib.auth import get_user_model
from utils.send_email import sp_send_simple_email

class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountFilterView(viewsets.ModelViewSet):
    queryset = AccountFilter.objects.all()
    serializer_class = AccountFilterSerializer

class AgeView(viewsets.ModelViewSet):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer

class GenderView(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

class IncomeView(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class OrderTypeView(viewsets.ModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer

class OrderStatusView(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class OrderDetailedView(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderDetailedSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(created_by=self.request.user)
        return queryset

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
        subject = 'Регистрация в приложении Геоаналитика'
        to_name = first_name + ' ' + last_name
        html = '<p>Уважаемый, ' + to_name + '! Ваш логин: ' + username + ', пароль: ' + password + '.</p>'
        text = 'Уважаемый, ' + to_name + '! Ваш логин: ' + username + ', пароль: ' + password + '. '
        sp_send_simple_email(subject, html, text, to_name, email)
        return Response(status=status.HTTP_201_CREATED)
    else:
        message = "user_exists"

    err = {
        "error": message
    }
    return Response(err, status=status.HTTP_400_BAD_REQUEST)