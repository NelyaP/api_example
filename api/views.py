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
    if not request.method == 'POST':
        return Response({"message": "Only POST method is available"}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'username' in request.data and request.data['username'] and \
        'phone' in request.data and request.data['phone'] and \
        'email' in request.data and request.data['email'] and \
        'alias_name' in request.data and request.data['alias_name'] and \
        'is_allowed' in request.data and request.data['is_allowed'] and \
        'company' in request.data and request.data['company']:

        username = request.data['username']
        phone = request.data['phone']
        email = request.data['email']
        alias_name = request.data['alias_name']
        first_name = None
        if 'first_name' in request.data and request.data['first_name']:
            first_name = request.data['first_name']
        last_name = None
        if 'last_name' in request.data and request.data['last_name']:
            last_name = request.data['last_name']
        month = None
        if 'month' in request.data and request.data['month']:
            last_name = request.data['month']
        is_allowed = request.data['is_allowed']
        company = request.data['company']

        User = get_user_model()
        password = generate_20char_pwd()
        if User.objects.filter(username=username).exists():
            return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(
            username=username, 
            password=password, 
            phone=phone, 
            alias_name=alias_name, 
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            month=month,
            is_allowed=is_allowed,
            company=company)
        # send email
        subject = 'Регистрация в приложении Геоаналитика'
        html = '<p>Уважаемый, ' + alias_name + '! Ваш логин: ' + username + ', пароль: ' + password + '.</p>'
        text = 'Уважаемый, ' + alias_name + '! Ваш логин: ' + username + ', пароль: ' + password + '. '
        sp_send_simple_email(subject, html, text, alias_name, email)
        return Response({"message": "User registared successfully"},status=status.HTTP_201_CREATED)